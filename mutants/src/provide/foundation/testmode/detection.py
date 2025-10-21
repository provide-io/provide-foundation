# provide/foundation/testmode/detection.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# detection.py
#
import inspect
import os
import sys

"""Test Mode Detection for Foundation.

This module provides utilities for detecting various test environments
and adjusting Foundation behavior accordingly.
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_is_in_test_mode__mutmut_orig() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_1() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "XXPYTEST_CURRENT_TESTXX" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_2() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "pytest_current_test" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_3() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" not in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_4() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return False

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_5() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "XXpytestXX" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_6() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "PYTEST" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_7() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" not in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_8() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any(None):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_9() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("XXpytestXX" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_10() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("PYTEST" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_11() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" not in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_12() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return False

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_13() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = None
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_14() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename and ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_15() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or "XXXX"
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_16() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename and "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_17() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename and "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_18() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "XXpytestXX" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_19() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "PYTEST" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_20() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" not in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_21() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "XX/test_XX" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_22() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/TEST_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_23() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" not in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_24() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "XXconftest.pyXX" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_25() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "CONFTEST.PY" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_26() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" not in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_27() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return False

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_28() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool(None)


def x_is_in_test_mode__mutmut_29() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules or any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_30() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("XXunittestXX" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_31() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("UNITTEST" in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_32() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" not in sys.modules and any("unittest" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_33() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any(None))


def x_is_in_test_mode__mutmut_34() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("XXunittestXX" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_35() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("UNITTEST" in arg for arg in sys.argv))


def x_is_in_test_mode__mutmut_36() -> bool:
    """Detect if we're running in a test environment.

    This method checks for common test environment indicators to determine
    if Foundation components should adjust their behavior for test compatibility.

    Returns:
        True if running in test mode, False otherwise
    """
    # Primary indicator: pytest current test environment variable
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # Check if pytest is currently imported and active
    if "pytest" in sys.modules:
        # Additional check: make sure we're actually running in a test context
        if any("pytest" in arg for arg in sys.argv):
            return True

        # Check if pytest is actively running by looking for test-related stack frames
        for frame_info in inspect.stack():
            filename = frame_info.filename or ""
            if "pytest" in filename or "/test_" in filename or "conftest.py" in filename:
                return True

    # Check for unittest runner in active execution
    return bool("unittest" in sys.modules and any("unittest" not in arg for arg in sys.argv))

x_is_in_test_mode__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_in_test_mode__mutmut_1': x_is_in_test_mode__mutmut_1, 
    'x_is_in_test_mode__mutmut_2': x_is_in_test_mode__mutmut_2, 
    'x_is_in_test_mode__mutmut_3': x_is_in_test_mode__mutmut_3, 
    'x_is_in_test_mode__mutmut_4': x_is_in_test_mode__mutmut_4, 
    'x_is_in_test_mode__mutmut_5': x_is_in_test_mode__mutmut_5, 
    'x_is_in_test_mode__mutmut_6': x_is_in_test_mode__mutmut_6, 
    'x_is_in_test_mode__mutmut_7': x_is_in_test_mode__mutmut_7, 
    'x_is_in_test_mode__mutmut_8': x_is_in_test_mode__mutmut_8, 
    'x_is_in_test_mode__mutmut_9': x_is_in_test_mode__mutmut_9, 
    'x_is_in_test_mode__mutmut_10': x_is_in_test_mode__mutmut_10, 
    'x_is_in_test_mode__mutmut_11': x_is_in_test_mode__mutmut_11, 
    'x_is_in_test_mode__mutmut_12': x_is_in_test_mode__mutmut_12, 
    'x_is_in_test_mode__mutmut_13': x_is_in_test_mode__mutmut_13, 
    'x_is_in_test_mode__mutmut_14': x_is_in_test_mode__mutmut_14, 
    'x_is_in_test_mode__mutmut_15': x_is_in_test_mode__mutmut_15, 
    'x_is_in_test_mode__mutmut_16': x_is_in_test_mode__mutmut_16, 
    'x_is_in_test_mode__mutmut_17': x_is_in_test_mode__mutmut_17, 
    'x_is_in_test_mode__mutmut_18': x_is_in_test_mode__mutmut_18, 
    'x_is_in_test_mode__mutmut_19': x_is_in_test_mode__mutmut_19, 
    'x_is_in_test_mode__mutmut_20': x_is_in_test_mode__mutmut_20, 
    'x_is_in_test_mode__mutmut_21': x_is_in_test_mode__mutmut_21, 
    'x_is_in_test_mode__mutmut_22': x_is_in_test_mode__mutmut_22, 
    'x_is_in_test_mode__mutmut_23': x_is_in_test_mode__mutmut_23, 
    'x_is_in_test_mode__mutmut_24': x_is_in_test_mode__mutmut_24, 
    'x_is_in_test_mode__mutmut_25': x_is_in_test_mode__mutmut_25, 
    'x_is_in_test_mode__mutmut_26': x_is_in_test_mode__mutmut_26, 
    'x_is_in_test_mode__mutmut_27': x_is_in_test_mode__mutmut_27, 
    'x_is_in_test_mode__mutmut_28': x_is_in_test_mode__mutmut_28, 
    'x_is_in_test_mode__mutmut_29': x_is_in_test_mode__mutmut_29, 
    'x_is_in_test_mode__mutmut_30': x_is_in_test_mode__mutmut_30, 
    'x_is_in_test_mode__mutmut_31': x_is_in_test_mode__mutmut_31, 
    'x_is_in_test_mode__mutmut_32': x_is_in_test_mode__mutmut_32, 
    'x_is_in_test_mode__mutmut_33': x_is_in_test_mode__mutmut_33, 
    'x_is_in_test_mode__mutmut_34': x_is_in_test_mode__mutmut_34, 
    'x_is_in_test_mode__mutmut_35': x_is_in_test_mode__mutmut_35, 
    'x_is_in_test_mode__mutmut_36': x_is_in_test_mode__mutmut_36
}

def is_in_test_mode(*args, **kwargs):
    result = _mutmut_trampoline(x_is_in_test_mode__mutmut_orig, x_is_in_test_mode__mutmut_mutants, args, kwargs)
    return result 

is_in_test_mode.__signature__ = _mutmut_signature(x_is_in_test_mode__mutmut_orig)
x_is_in_test_mode__mutmut_orig.__name__ = 'x_is_in_test_mode'


def x_is_in_click_testing__mutmut_orig() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_1() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = None

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_2() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return False

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_3() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = None
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_4() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get(None, "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_5() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", None)
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_6() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_7() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", )
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_8() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("XX__name__XX", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_9() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__NAME__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_10() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "XXXX")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_11() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = None

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_12() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename and ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_13() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or "XXXX"

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_14() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module and "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_15() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "XXclick.testingXX" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_16() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "CLICK.TESTING" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_17() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" not in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_18() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "XXtest_cli_integrationXX" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_19() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "TEST_CLI_INTEGRATION" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_20() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" not in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_21() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return False

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_22() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = None
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_23() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get(None)
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_24() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("XXselfXX")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_25() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("SELF")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_26() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None or hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_27() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_28() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(None, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_29() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, None):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_30() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr("runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_31() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, ):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_32() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "XXrunnerXX"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_33() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "RUNNER"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_34() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = None
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_35() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") or "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_36() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(None, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_37() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, None) and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_38() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr("invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_39() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, ) and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_40() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "XXinvokeXX") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_41() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "INVOKE") and "CliRunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_42() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "XXCliRunnerXX" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_43() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "clirunner" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_44() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CLIRUNNER" in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_45() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" not in str(type(runner)):
                return True

    return False


def x_is_in_click_testing__mutmut_46() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(None):
                return True

    return False


def x_is_in_click_testing__mutmut_47() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(None)):
                return True

    return False


def x_is_in_click_testing__mutmut_48() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return False

    return False


def x_is_in_click_testing__mutmut_49() -> bool:
    """Check if we're running inside Click's testing framework.

    This detects Click's CliRunner testing context to prevent stream
    manipulation that could interfere with Click's output capture.

    Returns:
        True if running in Click testing context, False otherwise
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if locals_self is not None and hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return True

x_is_in_click_testing__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_in_click_testing__mutmut_1': x_is_in_click_testing__mutmut_1, 
    'x_is_in_click_testing__mutmut_2': x_is_in_click_testing__mutmut_2, 
    'x_is_in_click_testing__mutmut_3': x_is_in_click_testing__mutmut_3, 
    'x_is_in_click_testing__mutmut_4': x_is_in_click_testing__mutmut_4, 
    'x_is_in_click_testing__mutmut_5': x_is_in_click_testing__mutmut_5, 
    'x_is_in_click_testing__mutmut_6': x_is_in_click_testing__mutmut_6, 
    'x_is_in_click_testing__mutmut_7': x_is_in_click_testing__mutmut_7, 
    'x_is_in_click_testing__mutmut_8': x_is_in_click_testing__mutmut_8, 
    'x_is_in_click_testing__mutmut_9': x_is_in_click_testing__mutmut_9, 
    'x_is_in_click_testing__mutmut_10': x_is_in_click_testing__mutmut_10, 
    'x_is_in_click_testing__mutmut_11': x_is_in_click_testing__mutmut_11, 
    'x_is_in_click_testing__mutmut_12': x_is_in_click_testing__mutmut_12, 
    'x_is_in_click_testing__mutmut_13': x_is_in_click_testing__mutmut_13, 
    'x_is_in_click_testing__mutmut_14': x_is_in_click_testing__mutmut_14, 
    'x_is_in_click_testing__mutmut_15': x_is_in_click_testing__mutmut_15, 
    'x_is_in_click_testing__mutmut_16': x_is_in_click_testing__mutmut_16, 
    'x_is_in_click_testing__mutmut_17': x_is_in_click_testing__mutmut_17, 
    'x_is_in_click_testing__mutmut_18': x_is_in_click_testing__mutmut_18, 
    'x_is_in_click_testing__mutmut_19': x_is_in_click_testing__mutmut_19, 
    'x_is_in_click_testing__mutmut_20': x_is_in_click_testing__mutmut_20, 
    'x_is_in_click_testing__mutmut_21': x_is_in_click_testing__mutmut_21, 
    'x_is_in_click_testing__mutmut_22': x_is_in_click_testing__mutmut_22, 
    'x_is_in_click_testing__mutmut_23': x_is_in_click_testing__mutmut_23, 
    'x_is_in_click_testing__mutmut_24': x_is_in_click_testing__mutmut_24, 
    'x_is_in_click_testing__mutmut_25': x_is_in_click_testing__mutmut_25, 
    'x_is_in_click_testing__mutmut_26': x_is_in_click_testing__mutmut_26, 
    'x_is_in_click_testing__mutmut_27': x_is_in_click_testing__mutmut_27, 
    'x_is_in_click_testing__mutmut_28': x_is_in_click_testing__mutmut_28, 
    'x_is_in_click_testing__mutmut_29': x_is_in_click_testing__mutmut_29, 
    'x_is_in_click_testing__mutmut_30': x_is_in_click_testing__mutmut_30, 
    'x_is_in_click_testing__mutmut_31': x_is_in_click_testing__mutmut_31, 
    'x_is_in_click_testing__mutmut_32': x_is_in_click_testing__mutmut_32, 
    'x_is_in_click_testing__mutmut_33': x_is_in_click_testing__mutmut_33, 
    'x_is_in_click_testing__mutmut_34': x_is_in_click_testing__mutmut_34, 
    'x_is_in_click_testing__mutmut_35': x_is_in_click_testing__mutmut_35, 
    'x_is_in_click_testing__mutmut_36': x_is_in_click_testing__mutmut_36, 
    'x_is_in_click_testing__mutmut_37': x_is_in_click_testing__mutmut_37, 
    'x_is_in_click_testing__mutmut_38': x_is_in_click_testing__mutmut_38, 
    'x_is_in_click_testing__mutmut_39': x_is_in_click_testing__mutmut_39, 
    'x_is_in_click_testing__mutmut_40': x_is_in_click_testing__mutmut_40, 
    'x_is_in_click_testing__mutmut_41': x_is_in_click_testing__mutmut_41, 
    'x_is_in_click_testing__mutmut_42': x_is_in_click_testing__mutmut_42, 
    'x_is_in_click_testing__mutmut_43': x_is_in_click_testing__mutmut_43, 
    'x_is_in_click_testing__mutmut_44': x_is_in_click_testing__mutmut_44, 
    'x_is_in_click_testing__mutmut_45': x_is_in_click_testing__mutmut_45, 
    'x_is_in_click_testing__mutmut_46': x_is_in_click_testing__mutmut_46, 
    'x_is_in_click_testing__mutmut_47': x_is_in_click_testing__mutmut_47, 
    'x_is_in_click_testing__mutmut_48': x_is_in_click_testing__mutmut_48, 
    'x_is_in_click_testing__mutmut_49': x_is_in_click_testing__mutmut_49
}

def is_in_click_testing(*args, **kwargs):
    result = _mutmut_trampoline(x_is_in_click_testing__mutmut_orig, x_is_in_click_testing__mutmut_mutants, args, kwargs)
    return result 

is_in_click_testing.__signature__ = _mutmut_signature(x_is_in_click_testing__mutmut_orig)
x_is_in_click_testing__mutmut_orig.__name__ = 'x_is_in_click_testing'


def x_should_allow_stream_redirect__mutmut_orig() -> bool:
    """Check if stream redirection should be allowed in testing.

    Stream redirection is normally blocked when in Click testing context
    to prevent interference with Click's output capture. This can be
    overridden with FOUNDATION_FORCE_STREAM_REDIRECT=true.

    Returns:
        True if stream redirect is allowed (not in Click testing OR force enabled)
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Allow if force flag is set
    if config.force_stream_redirect:
        return True

    # Otherwise, block if in Click testing
    return not is_in_click_testing()


def x_should_allow_stream_redirect__mutmut_1() -> bool:
    """Check if stream redirection should be allowed in testing.

    Stream redirection is normally blocked when in Click testing context
    to prevent interference with Click's output capture. This can be
    overridden with FOUNDATION_FORCE_STREAM_REDIRECT=true.

    Returns:
        True if stream redirect is allowed (not in Click testing OR force enabled)
    """
    from provide.foundation.streams.config import get_stream_config

    config = None

    # Allow if force flag is set
    if config.force_stream_redirect:
        return True

    # Otherwise, block if in Click testing
    return not is_in_click_testing()


def x_should_allow_stream_redirect__mutmut_2() -> bool:
    """Check if stream redirection should be allowed in testing.

    Stream redirection is normally blocked when in Click testing context
    to prevent interference with Click's output capture. This can be
    overridden with FOUNDATION_FORCE_STREAM_REDIRECT=true.

    Returns:
        True if stream redirect is allowed (not in Click testing OR force enabled)
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Allow if force flag is set
    if config.force_stream_redirect:
        return False

    # Otherwise, block if in Click testing
    return not is_in_click_testing()


def x_should_allow_stream_redirect__mutmut_3() -> bool:
    """Check if stream redirection should be allowed in testing.

    Stream redirection is normally blocked when in Click testing context
    to prevent interference with Click's output capture. This can be
    overridden with FOUNDATION_FORCE_STREAM_REDIRECT=true.

    Returns:
        True if stream redirect is allowed (not in Click testing OR force enabled)
    """
    from provide.foundation.streams.config import get_stream_config

    config = get_stream_config()

    # Allow if force flag is set
    if config.force_stream_redirect:
        return True

    # Otherwise, block if in Click testing
    return is_in_click_testing()

x_should_allow_stream_redirect__mutmut_mutants : ClassVar[MutantDict] = {
'x_should_allow_stream_redirect__mutmut_1': x_should_allow_stream_redirect__mutmut_1, 
    'x_should_allow_stream_redirect__mutmut_2': x_should_allow_stream_redirect__mutmut_2, 
    'x_should_allow_stream_redirect__mutmut_3': x_should_allow_stream_redirect__mutmut_3
}

def should_allow_stream_redirect(*args, **kwargs):
    result = _mutmut_trampoline(x_should_allow_stream_redirect__mutmut_orig, x_should_allow_stream_redirect__mutmut_mutants, args, kwargs)
    return result 

should_allow_stream_redirect.__signature__ = _mutmut_signature(x_should_allow_stream_redirect__mutmut_orig)
x_should_allow_stream_redirect__mutmut_orig.__name__ = 'x_should_allow_stream_redirect'


def should_use_shared_registries(
    use_shared_registries: bool,
    component_registry: object | None,
    command_registry: object | None,
) -> bool:
    """Determine if Hub should use shared registries based on explicit parameters.

    Args:
        use_shared_registries: Explicit user preference
        component_registry: Custom component registry if provided
        command_registry: Custom command registry if provided

    Returns:
        True if shared registries should be used
    """
    # Return explicit preference - no auto-detection magic
    return use_shared_registries


def x_configure_structlog_for_test_safety__mutmut_orig() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_1() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=None,
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_2() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=None,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_3() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=None,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_4() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=None,
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_5() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=None,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_6() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_7() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_8() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_9() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_10() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        )


def x_configure_structlog_for_test_safety__mutmut_11() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt=None),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_12() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="XXisoXX"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_13() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_14() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(None),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_15() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=None),
        cache_logger_on_first_use=False,  # Disable caching for test isolation
    )


def x_configure_structlog_for_test_safety__mutmut_16() -> None:
    """Configure structlog to use stdout for multiprocessing safety.

    When running tests with parallel execution (pytest-xdist, mutmut with
    --max-children, etc.), file handles don't survive process forking.
    This causes "I/O operation on closed file" errors when structlog's
    PrintLogger tries to write to file handles from forked processes.

    This function configures structlog to use sys.stdout which is safe
    for multiprocessing and properly handled by pytest.

    Should be called automatically when is_in_test_mode() returns True.
    """
    import logging as stdlib_logging
    import sys

    import structlog

    # Configure structlog to use stdout (safe for multiprocessing)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(stdlib_logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,  # Disable caching for test isolation
    )

x_configure_structlog_for_test_safety__mutmut_mutants : ClassVar[MutantDict] = {
'x_configure_structlog_for_test_safety__mutmut_1': x_configure_structlog_for_test_safety__mutmut_1, 
    'x_configure_structlog_for_test_safety__mutmut_2': x_configure_structlog_for_test_safety__mutmut_2, 
    'x_configure_structlog_for_test_safety__mutmut_3': x_configure_structlog_for_test_safety__mutmut_3, 
    'x_configure_structlog_for_test_safety__mutmut_4': x_configure_structlog_for_test_safety__mutmut_4, 
    'x_configure_structlog_for_test_safety__mutmut_5': x_configure_structlog_for_test_safety__mutmut_5, 
    'x_configure_structlog_for_test_safety__mutmut_6': x_configure_structlog_for_test_safety__mutmut_6, 
    'x_configure_structlog_for_test_safety__mutmut_7': x_configure_structlog_for_test_safety__mutmut_7, 
    'x_configure_structlog_for_test_safety__mutmut_8': x_configure_structlog_for_test_safety__mutmut_8, 
    'x_configure_structlog_for_test_safety__mutmut_9': x_configure_structlog_for_test_safety__mutmut_9, 
    'x_configure_structlog_for_test_safety__mutmut_10': x_configure_structlog_for_test_safety__mutmut_10, 
    'x_configure_structlog_for_test_safety__mutmut_11': x_configure_structlog_for_test_safety__mutmut_11, 
    'x_configure_structlog_for_test_safety__mutmut_12': x_configure_structlog_for_test_safety__mutmut_12, 
    'x_configure_structlog_for_test_safety__mutmut_13': x_configure_structlog_for_test_safety__mutmut_13, 
    'x_configure_structlog_for_test_safety__mutmut_14': x_configure_structlog_for_test_safety__mutmut_14, 
    'x_configure_structlog_for_test_safety__mutmut_15': x_configure_structlog_for_test_safety__mutmut_15, 
    'x_configure_structlog_for_test_safety__mutmut_16': x_configure_structlog_for_test_safety__mutmut_16
}

def configure_structlog_for_test_safety(*args, **kwargs):
    result = _mutmut_trampoline(x_configure_structlog_for_test_safety__mutmut_orig, x_configure_structlog_for_test_safety__mutmut_mutants, args, kwargs)
    return result 

configure_structlog_for_test_safety.__signature__ = _mutmut_signature(x_configure_structlog_for_test_safety__mutmut_orig)
x_configure_structlog_for_test_safety__mutmut_orig.__name__ = 'x_configure_structlog_for_test_safety'


# <3 🧱🤝🧪🪄
