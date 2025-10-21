# provide/foundation/file/operations/detectors/helpers.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Shared helper functions for file operation detectors."""

from __future__ import annotations

from pathlib import Path
import re
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


def x_is_temp_file__mutmut_orig(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_1(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = None
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_2(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.upper()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_3(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.upper()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_4(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if "XX.tmp.XX" in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_5(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".TMP." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_6(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." not in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_7(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return False

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_8(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = None

    return any(temp_patterns)


def x_is_temp_file__mutmut_9(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(None),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_10(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith("XX.tmpXX"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_11(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".TMP"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_12(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith(None),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_13(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("XXtmpXX"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_14(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("TMP"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_15(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(None),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_16(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith("XX.tmpXX"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_17(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".TMP"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_18(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(None),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_19(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith("XX.tempXX"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_20(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".TEMP"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_21(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith(None),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_22(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("XX~XX"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_23(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        "XX.swpXX" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_24(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".SWP" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_25(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" not in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_26(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        "XX.swxXX" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_27(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".SWX" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_28(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" not in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_29(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        "XX.swoXX" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_30(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".SWO" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_31(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" not in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_32(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(None),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_33(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith("XX.swnXX"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_34(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".SWN"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_35(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        "XX.#XX" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_36(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" not in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_37(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") or name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_38(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith(None) and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_39(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("XX#XX") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_40(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith(None),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_41(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("XX#XX"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_42(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(None),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_43(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith("XX.bakXX"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_44(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".BAK"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_45(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(None),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_46(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith("XX.backupXX"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_47(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".BACKUP"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_48(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(None),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_49(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith("XX.origXX"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_50(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".ORIG"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_51(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(None),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_52(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("XX.oldXX"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_53(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".OLD"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_54(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        "XX.$XX" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_55(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" not in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_56(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith(None),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_57(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("XX~$XX"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_58(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        "XX.cacheXX" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_59(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".CACHE" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_60(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" not in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_61(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name or not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_62(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        "XX.lockXX" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_63(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".LOCK" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_64(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" not in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_65(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_66(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(None),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_67(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith("XX.lockXX"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_68(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".LOCK"),  # .lock.123 but not package.lock
    ]

    return any(temp_patterns)


def x_is_temp_file__mutmut_69(path: Path) -> bool:
    """Check if path looks like a temporary file.

    Detects temp files from various sources:
    - Editors: VSCode, Vim, Emacs, Sublime, etc.
    - Build tools: Python tempfile, system tmp, etc.
    - Atomic write patterns: .tmp.{PID}.{timestamp}
    """
    name = path.name.lower()
    path.stem.lower()

    # BROAD PATTERN: Any file with .tmp. followed by anything
    # Catches: filename.tmp.123, filename.tmp.58540.1760056690894, .file.tmp.84
    # This is the most important pattern - covers most atomic write patterns
    if ".tmp." in name:
        return True

    # Editor-specific patterns
    temp_patterns = [
        # Generic temp markers
        name.startswith(".tmp"),
        name.startswith("tmp"),
        name.endswith(".tmp"),
        name.endswith(".temp"),
        name.endswith("~"),
        # Vim swap files
        ".swp" in name,
        ".swx" in name,
        ".swo" in name,
        name.endswith(".swn"),
        # Emacs temp files
        ".#" in name,
        name.startswith("#") and name.endswith("#"),
        # Backup files
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(".old"),
        # System temp markers
        ".$" in name,  # Windows
        name.startswith("~$"),  # Office temp files
        # Build/cache artifacts (common patterns)
        ".cache" in name,
        ".lock" in name and not name.endswith(".lock"),  # .lock.123 but not package.lock
    ]

    return any(None)

x_is_temp_file__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_temp_file__mutmut_1': x_is_temp_file__mutmut_1, 
    'x_is_temp_file__mutmut_2': x_is_temp_file__mutmut_2, 
    'x_is_temp_file__mutmut_3': x_is_temp_file__mutmut_3, 
    'x_is_temp_file__mutmut_4': x_is_temp_file__mutmut_4, 
    'x_is_temp_file__mutmut_5': x_is_temp_file__mutmut_5, 
    'x_is_temp_file__mutmut_6': x_is_temp_file__mutmut_6, 
    'x_is_temp_file__mutmut_7': x_is_temp_file__mutmut_7, 
    'x_is_temp_file__mutmut_8': x_is_temp_file__mutmut_8, 
    'x_is_temp_file__mutmut_9': x_is_temp_file__mutmut_9, 
    'x_is_temp_file__mutmut_10': x_is_temp_file__mutmut_10, 
    'x_is_temp_file__mutmut_11': x_is_temp_file__mutmut_11, 
    'x_is_temp_file__mutmut_12': x_is_temp_file__mutmut_12, 
    'x_is_temp_file__mutmut_13': x_is_temp_file__mutmut_13, 
    'x_is_temp_file__mutmut_14': x_is_temp_file__mutmut_14, 
    'x_is_temp_file__mutmut_15': x_is_temp_file__mutmut_15, 
    'x_is_temp_file__mutmut_16': x_is_temp_file__mutmut_16, 
    'x_is_temp_file__mutmut_17': x_is_temp_file__mutmut_17, 
    'x_is_temp_file__mutmut_18': x_is_temp_file__mutmut_18, 
    'x_is_temp_file__mutmut_19': x_is_temp_file__mutmut_19, 
    'x_is_temp_file__mutmut_20': x_is_temp_file__mutmut_20, 
    'x_is_temp_file__mutmut_21': x_is_temp_file__mutmut_21, 
    'x_is_temp_file__mutmut_22': x_is_temp_file__mutmut_22, 
    'x_is_temp_file__mutmut_23': x_is_temp_file__mutmut_23, 
    'x_is_temp_file__mutmut_24': x_is_temp_file__mutmut_24, 
    'x_is_temp_file__mutmut_25': x_is_temp_file__mutmut_25, 
    'x_is_temp_file__mutmut_26': x_is_temp_file__mutmut_26, 
    'x_is_temp_file__mutmut_27': x_is_temp_file__mutmut_27, 
    'x_is_temp_file__mutmut_28': x_is_temp_file__mutmut_28, 
    'x_is_temp_file__mutmut_29': x_is_temp_file__mutmut_29, 
    'x_is_temp_file__mutmut_30': x_is_temp_file__mutmut_30, 
    'x_is_temp_file__mutmut_31': x_is_temp_file__mutmut_31, 
    'x_is_temp_file__mutmut_32': x_is_temp_file__mutmut_32, 
    'x_is_temp_file__mutmut_33': x_is_temp_file__mutmut_33, 
    'x_is_temp_file__mutmut_34': x_is_temp_file__mutmut_34, 
    'x_is_temp_file__mutmut_35': x_is_temp_file__mutmut_35, 
    'x_is_temp_file__mutmut_36': x_is_temp_file__mutmut_36, 
    'x_is_temp_file__mutmut_37': x_is_temp_file__mutmut_37, 
    'x_is_temp_file__mutmut_38': x_is_temp_file__mutmut_38, 
    'x_is_temp_file__mutmut_39': x_is_temp_file__mutmut_39, 
    'x_is_temp_file__mutmut_40': x_is_temp_file__mutmut_40, 
    'x_is_temp_file__mutmut_41': x_is_temp_file__mutmut_41, 
    'x_is_temp_file__mutmut_42': x_is_temp_file__mutmut_42, 
    'x_is_temp_file__mutmut_43': x_is_temp_file__mutmut_43, 
    'x_is_temp_file__mutmut_44': x_is_temp_file__mutmut_44, 
    'x_is_temp_file__mutmut_45': x_is_temp_file__mutmut_45, 
    'x_is_temp_file__mutmut_46': x_is_temp_file__mutmut_46, 
    'x_is_temp_file__mutmut_47': x_is_temp_file__mutmut_47, 
    'x_is_temp_file__mutmut_48': x_is_temp_file__mutmut_48, 
    'x_is_temp_file__mutmut_49': x_is_temp_file__mutmut_49, 
    'x_is_temp_file__mutmut_50': x_is_temp_file__mutmut_50, 
    'x_is_temp_file__mutmut_51': x_is_temp_file__mutmut_51, 
    'x_is_temp_file__mutmut_52': x_is_temp_file__mutmut_52, 
    'x_is_temp_file__mutmut_53': x_is_temp_file__mutmut_53, 
    'x_is_temp_file__mutmut_54': x_is_temp_file__mutmut_54, 
    'x_is_temp_file__mutmut_55': x_is_temp_file__mutmut_55, 
    'x_is_temp_file__mutmut_56': x_is_temp_file__mutmut_56, 
    'x_is_temp_file__mutmut_57': x_is_temp_file__mutmut_57, 
    'x_is_temp_file__mutmut_58': x_is_temp_file__mutmut_58, 
    'x_is_temp_file__mutmut_59': x_is_temp_file__mutmut_59, 
    'x_is_temp_file__mutmut_60': x_is_temp_file__mutmut_60, 
    'x_is_temp_file__mutmut_61': x_is_temp_file__mutmut_61, 
    'x_is_temp_file__mutmut_62': x_is_temp_file__mutmut_62, 
    'x_is_temp_file__mutmut_63': x_is_temp_file__mutmut_63, 
    'x_is_temp_file__mutmut_64': x_is_temp_file__mutmut_64, 
    'x_is_temp_file__mutmut_65': x_is_temp_file__mutmut_65, 
    'x_is_temp_file__mutmut_66': x_is_temp_file__mutmut_66, 
    'x_is_temp_file__mutmut_67': x_is_temp_file__mutmut_67, 
    'x_is_temp_file__mutmut_68': x_is_temp_file__mutmut_68, 
    'x_is_temp_file__mutmut_69': x_is_temp_file__mutmut_69
}

def is_temp_file(*args, **kwargs):
    result = _mutmut_trampoline(x_is_temp_file__mutmut_orig, x_is_temp_file__mutmut_mutants, args, kwargs)
    return result 

is_temp_file.__signature__ = _mutmut_signature(x_is_temp_file__mutmut_orig)
x_is_temp_file__mutmut_orig.__name__ = 'x_is_temp_file'


def x_is_backup_file__mutmut_orig(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_1(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = None

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_2(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.upper()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_3(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = None

    return any(backup_patterns)


def x_is_backup_file__mutmut_4(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(None),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_5(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith("XX.bakXX"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_6(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".BAK"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_7(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(None),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_8(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith("XX.backupXX"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_9(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".BACKUP"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_10(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(None),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_11(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith("XX.origXX"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_12(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".ORIG"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_13(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith(None),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_14(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("XX~XX"),
        ".bak." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_15(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        "XX.bak.XX" in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_16(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".BAK." in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_17(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." not in name,
    ]

    return any(backup_patterns)


def x_is_backup_file__mutmut_18(path: Path) -> bool:
    """Check if path looks like a backup file."""
    name = path.name.lower()

    backup_patterns = [
        name.endswith(".bak"),
        name.endswith(".backup"),
        name.endswith(".orig"),
        name.endswith("~"),
        ".bak." in name,
    ]

    return any(None)

x_is_backup_file__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_backup_file__mutmut_1': x_is_backup_file__mutmut_1, 
    'x_is_backup_file__mutmut_2': x_is_backup_file__mutmut_2, 
    'x_is_backup_file__mutmut_3': x_is_backup_file__mutmut_3, 
    'x_is_backup_file__mutmut_4': x_is_backup_file__mutmut_4, 
    'x_is_backup_file__mutmut_5': x_is_backup_file__mutmut_5, 
    'x_is_backup_file__mutmut_6': x_is_backup_file__mutmut_6, 
    'x_is_backup_file__mutmut_7': x_is_backup_file__mutmut_7, 
    'x_is_backup_file__mutmut_8': x_is_backup_file__mutmut_8, 
    'x_is_backup_file__mutmut_9': x_is_backup_file__mutmut_9, 
    'x_is_backup_file__mutmut_10': x_is_backup_file__mutmut_10, 
    'x_is_backup_file__mutmut_11': x_is_backup_file__mutmut_11, 
    'x_is_backup_file__mutmut_12': x_is_backup_file__mutmut_12, 
    'x_is_backup_file__mutmut_13': x_is_backup_file__mutmut_13, 
    'x_is_backup_file__mutmut_14': x_is_backup_file__mutmut_14, 
    'x_is_backup_file__mutmut_15': x_is_backup_file__mutmut_15, 
    'x_is_backup_file__mutmut_16': x_is_backup_file__mutmut_16, 
    'x_is_backup_file__mutmut_17': x_is_backup_file__mutmut_17, 
    'x_is_backup_file__mutmut_18': x_is_backup_file__mutmut_18
}

def is_backup_file(*args, **kwargs):
    result = _mutmut_trampoline(x_is_backup_file__mutmut_orig, x_is_backup_file__mutmut_mutants, args, kwargs)
    return result 

is_backup_file.__signature__ = _mutmut_signature(x_is_backup_file__mutmut_orig)
x_is_backup_file__mutmut_orig.__name__ = 'x_is_backup_file'


def x_extract_base_name__mutmut_orig(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_1(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = None

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_2(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = None

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_3(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = None
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_4(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"XX^\.(.+)\.tmp\.\w+$XX"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_5(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_6(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.TMP\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_7(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(None, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_8(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, None):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_9(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_10(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, ):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_11(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = None
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_12(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(None, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_13(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, None, base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_14(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", None)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_15(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_16(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_17(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", )
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_18(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"XX\1XX", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_19(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_20(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_21(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") or base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_22(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith(None) and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_23(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("XX#XX") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_24(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith(None):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_25(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("XX#XX"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_26(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = None
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_27(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[2:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_28(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:+1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_29(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-2]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_30(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = None
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_31(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"XX^\.\.(.+)\.(swp|swo|swx)$XX"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_32(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_33(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(SWP|SWO|SWX)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_34(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = None
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_35(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(None, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_36(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, None)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_37(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_38(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, )
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_39(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = None
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_40(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." - match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_41(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "XX.XX" + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_42(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(None)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_43(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(2)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_44(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename or filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_45(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename == base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_46(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = None
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_47(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"XX^\.(.+)\.(swp|swo|swx)$XX"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_48(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_49(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(SWP|SWO|SWX)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_50(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = None
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_51(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(None, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_52(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, None)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_53(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_54(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, )
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_55(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = None
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_56(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(None)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_57(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(2)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_58(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename or filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_59(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename == base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_60(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = None

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_61(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = ["XX.tmpXX", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_62(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".TMP", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_63(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", "XX.tempXX", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_64(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".TEMP", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_65(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", "XX.bakXX", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_66(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".BAK", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_67(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", "XX.backupXX", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_68(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".BACKUP", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_69(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", "XX.origXX", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_70(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".ORIG", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_71(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "XX~XX"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_72(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(None):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_73(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = None
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_74(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: +len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_75(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            return

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_76(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = None
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_77(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["XXtmpXX", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_78(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["TMP", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_79(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", "XX.tmpXX", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_80(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".TMP", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_81(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", "XX.#XX"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_82(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(None):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_83(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = None
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_84(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            return

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_85(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = None

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_86(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(None, "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_87(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", None, base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_88(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", None)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_89(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub("", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_90(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_91(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", )

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_92(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"XX\.tmp\.\w+$XX", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_93(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_94(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.TMP\.\w+$", "", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_95(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "XXXX", base_name)

    return base_name if base_name and base_name != name else None


def x_extract_base_name__mutmut_96(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name or base_name != name else None


def x_extract_base_name__mutmut_97(path: Path) -> str | None:
    """Extract base filename for grouping related files.

    Removes temp/backup suffixes and prefixes to find the original filename.
    Returns None if no temp/backup pattern is found.
    """
    name = path.name

    base_name = name

    # Handle VSCode temp pattern FIRST: .filename.ext.tmp.XXXX -> filename.ext
    # This must come before other patterns since the leading dot is part of the temp name
    vscode_pattern = r"^\.(.+)\.tmp\.\w+$"
    if re.match(vscode_pattern, base_name):
        base_name = re.sub(vscode_pattern, r"\1", base_name)
        return base_name if base_name else None

    # Handle emacs autosave files: #document.txt# -> document.txt
    if base_name.startswith("#") and base_name.endswith("#"):
        base_name = base_name[1:-1]
        return base_name if base_name else None

    # Handle vim swap files:
    # - Regular file (document.txt) -> .document.txt.swp
    # - Dotfile (.document.txt) -> ..document.txt.swp (double leading dot)

    # First check for dotfile pattern (double dot)
    vim_dotfile_pattern = r"^\.\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_dotfile_pattern, base_name)
    if match:
        filename = "." + match.group(1)
        return filename if filename and filename != base_name else None

    # Then check for regular file pattern (single dot)
    vim_swap_pattern = r"^\.(.+)\.(swp|swo|swx)$"
    match = re.match(vim_swap_pattern, base_name)
    if match:
        filename = match.group(1)
        return filename if filename and filename != base_name else None

    # Remove common temp/backup suffixes
    suffixes_to_remove = [".tmp", ".temp", ".bak", ".backup", ".orig", "~"]

    for suffix in suffixes_to_remove:
        if base_name.endswith(suffix):
            base_name = base_name[: -len(suffix)]
            break

    # Remove temp prefixes
    prefixes_to_remove = ["tmp", ".tmp", ".#"]
    for prefix in prefixes_to_remove:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix) :]
            break

    # Remove temp file ID patterns like .tmp.84 (for any remaining patterns)
    base_name = re.sub(r"\.tmp\.\w+$", "", base_name)

    return base_name if base_name and base_name == name else None

x_extract_base_name__mutmut_mutants : ClassVar[MutantDict] = {
'x_extract_base_name__mutmut_1': x_extract_base_name__mutmut_1, 
    'x_extract_base_name__mutmut_2': x_extract_base_name__mutmut_2, 
    'x_extract_base_name__mutmut_3': x_extract_base_name__mutmut_3, 
    'x_extract_base_name__mutmut_4': x_extract_base_name__mutmut_4, 
    'x_extract_base_name__mutmut_5': x_extract_base_name__mutmut_5, 
    'x_extract_base_name__mutmut_6': x_extract_base_name__mutmut_6, 
    'x_extract_base_name__mutmut_7': x_extract_base_name__mutmut_7, 
    'x_extract_base_name__mutmut_8': x_extract_base_name__mutmut_8, 
    'x_extract_base_name__mutmut_9': x_extract_base_name__mutmut_9, 
    'x_extract_base_name__mutmut_10': x_extract_base_name__mutmut_10, 
    'x_extract_base_name__mutmut_11': x_extract_base_name__mutmut_11, 
    'x_extract_base_name__mutmut_12': x_extract_base_name__mutmut_12, 
    'x_extract_base_name__mutmut_13': x_extract_base_name__mutmut_13, 
    'x_extract_base_name__mutmut_14': x_extract_base_name__mutmut_14, 
    'x_extract_base_name__mutmut_15': x_extract_base_name__mutmut_15, 
    'x_extract_base_name__mutmut_16': x_extract_base_name__mutmut_16, 
    'x_extract_base_name__mutmut_17': x_extract_base_name__mutmut_17, 
    'x_extract_base_name__mutmut_18': x_extract_base_name__mutmut_18, 
    'x_extract_base_name__mutmut_19': x_extract_base_name__mutmut_19, 
    'x_extract_base_name__mutmut_20': x_extract_base_name__mutmut_20, 
    'x_extract_base_name__mutmut_21': x_extract_base_name__mutmut_21, 
    'x_extract_base_name__mutmut_22': x_extract_base_name__mutmut_22, 
    'x_extract_base_name__mutmut_23': x_extract_base_name__mutmut_23, 
    'x_extract_base_name__mutmut_24': x_extract_base_name__mutmut_24, 
    'x_extract_base_name__mutmut_25': x_extract_base_name__mutmut_25, 
    'x_extract_base_name__mutmut_26': x_extract_base_name__mutmut_26, 
    'x_extract_base_name__mutmut_27': x_extract_base_name__mutmut_27, 
    'x_extract_base_name__mutmut_28': x_extract_base_name__mutmut_28, 
    'x_extract_base_name__mutmut_29': x_extract_base_name__mutmut_29, 
    'x_extract_base_name__mutmut_30': x_extract_base_name__mutmut_30, 
    'x_extract_base_name__mutmut_31': x_extract_base_name__mutmut_31, 
    'x_extract_base_name__mutmut_32': x_extract_base_name__mutmut_32, 
    'x_extract_base_name__mutmut_33': x_extract_base_name__mutmut_33, 
    'x_extract_base_name__mutmut_34': x_extract_base_name__mutmut_34, 
    'x_extract_base_name__mutmut_35': x_extract_base_name__mutmut_35, 
    'x_extract_base_name__mutmut_36': x_extract_base_name__mutmut_36, 
    'x_extract_base_name__mutmut_37': x_extract_base_name__mutmut_37, 
    'x_extract_base_name__mutmut_38': x_extract_base_name__mutmut_38, 
    'x_extract_base_name__mutmut_39': x_extract_base_name__mutmut_39, 
    'x_extract_base_name__mutmut_40': x_extract_base_name__mutmut_40, 
    'x_extract_base_name__mutmut_41': x_extract_base_name__mutmut_41, 
    'x_extract_base_name__mutmut_42': x_extract_base_name__mutmut_42, 
    'x_extract_base_name__mutmut_43': x_extract_base_name__mutmut_43, 
    'x_extract_base_name__mutmut_44': x_extract_base_name__mutmut_44, 
    'x_extract_base_name__mutmut_45': x_extract_base_name__mutmut_45, 
    'x_extract_base_name__mutmut_46': x_extract_base_name__mutmut_46, 
    'x_extract_base_name__mutmut_47': x_extract_base_name__mutmut_47, 
    'x_extract_base_name__mutmut_48': x_extract_base_name__mutmut_48, 
    'x_extract_base_name__mutmut_49': x_extract_base_name__mutmut_49, 
    'x_extract_base_name__mutmut_50': x_extract_base_name__mutmut_50, 
    'x_extract_base_name__mutmut_51': x_extract_base_name__mutmut_51, 
    'x_extract_base_name__mutmut_52': x_extract_base_name__mutmut_52, 
    'x_extract_base_name__mutmut_53': x_extract_base_name__mutmut_53, 
    'x_extract_base_name__mutmut_54': x_extract_base_name__mutmut_54, 
    'x_extract_base_name__mutmut_55': x_extract_base_name__mutmut_55, 
    'x_extract_base_name__mutmut_56': x_extract_base_name__mutmut_56, 
    'x_extract_base_name__mutmut_57': x_extract_base_name__mutmut_57, 
    'x_extract_base_name__mutmut_58': x_extract_base_name__mutmut_58, 
    'x_extract_base_name__mutmut_59': x_extract_base_name__mutmut_59, 
    'x_extract_base_name__mutmut_60': x_extract_base_name__mutmut_60, 
    'x_extract_base_name__mutmut_61': x_extract_base_name__mutmut_61, 
    'x_extract_base_name__mutmut_62': x_extract_base_name__mutmut_62, 
    'x_extract_base_name__mutmut_63': x_extract_base_name__mutmut_63, 
    'x_extract_base_name__mutmut_64': x_extract_base_name__mutmut_64, 
    'x_extract_base_name__mutmut_65': x_extract_base_name__mutmut_65, 
    'x_extract_base_name__mutmut_66': x_extract_base_name__mutmut_66, 
    'x_extract_base_name__mutmut_67': x_extract_base_name__mutmut_67, 
    'x_extract_base_name__mutmut_68': x_extract_base_name__mutmut_68, 
    'x_extract_base_name__mutmut_69': x_extract_base_name__mutmut_69, 
    'x_extract_base_name__mutmut_70': x_extract_base_name__mutmut_70, 
    'x_extract_base_name__mutmut_71': x_extract_base_name__mutmut_71, 
    'x_extract_base_name__mutmut_72': x_extract_base_name__mutmut_72, 
    'x_extract_base_name__mutmut_73': x_extract_base_name__mutmut_73, 
    'x_extract_base_name__mutmut_74': x_extract_base_name__mutmut_74, 
    'x_extract_base_name__mutmut_75': x_extract_base_name__mutmut_75, 
    'x_extract_base_name__mutmut_76': x_extract_base_name__mutmut_76, 
    'x_extract_base_name__mutmut_77': x_extract_base_name__mutmut_77, 
    'x_extract_base_name__mutmut_78': x_extract_base_name__mutmut_78, 
    'x_extract_base_name__mutmut_79': x_extract_base_name__mutmut_79, 
    'x_extract_base_name__mutmut_80': x_extract_base_name__mutmut_80, 
    'x_extract_base_name__mutmut_81': x_extract_base_name__mutmut_81, 
    'x_extract_base_name__mutmut_82': x_extract_base_name__mutmut_82, 
    'x_extract_base_name__mutmut_83': x_extract_base_name__mutmut_83, 
    'x_extract_base_name__mutmut_84': x_extract_base_name__mutmut_84, 
    'x_extract_base_name__mutmut_85': x_extract_base_name__mutmut_85, 
    'x_extract_base_name__mutmut_86': x_extract_base_name__mutmut_86, 
    'x_extract_base_name__mutmut_87': x_extract_base_name__mutmut_87, 
    'x_extract_base_name__mutmut_88': x_extract_base_name__mutmut_88, 
    'x_extract_base_name__mutmut_89': x_extract_base_name__mutmut_89, 
    'x_extract_base_name__mutmut_90': x_extract_base_name__mutmut_90, 
    'x_extract_base_name__mutmut_91': x_extract_base_name__mutmut_91, 
    'x_extract_base_name__mutmut_92': x_extract_base_name__mutmut_92, 
    'x_extract_base_name__mutmut_93': x_extract_base_name__mutmut_93, 
    'x_extract_base_name__mutmut_94': x_extract_base_name__mutmut_94, 
    'x_extract_base_name__mutmut_95': x_extract_base_name__mutmut_95, 
    'x_extract_base_name__mutmut_96': x_extract_base_name__mutmut_96, 
    'x_extract_base_name__mutmut_97': x_extract_base_name__mutmut_97
}

def extract_base_name(*args, **kwargs):
    result = _mutmut_trampoline(x_extract_base_name__mutmut_orig, x_extract_base_name__mutmut_mutants, args, kwargs)
    return result 

extract_base_name.__signature__ = _mutmut_signature(x_extract_base_name__mutmut_orig)
x_extract_base_name__mutmut_orig.__name__ = 'x_extract_base_name'


def x_find_real_file_from_events__mutmut_orig(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_1(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(None):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_2(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path or not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_3(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") or event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_4(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(None, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_5(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, None) and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_6(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr("dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_7(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, ) and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_8(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "XXdest_pathXX") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_9(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "DEST_PATH") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_10(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_11(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(None):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_12(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_13(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(None):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_14(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") or event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_15(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(None, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_16(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, None) and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_17(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr("dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_18(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, ) and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_19(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "XXdest_pathXX") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_20(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "DEST_PATH") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_21(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = None
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_22(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(None)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_23(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = None
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_24(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent * base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_25(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path == event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_26(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = None
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_27(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(None)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_28(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = None
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_29(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent * base_name
            if real_path != event.path:
                return real_path

    return None


def x_find_real_file_from_events__mutmut_30(events: list) -> Path | None:
    """Find the real (non-temp) file path from a list of events.

    Args:
        events: List of FileEvent objects

    Returns:
        Real file path if found, None otherwise
    """
    # Look for non-temp files in the events
    for event in reversed(events):  # Start from most recent
        # Check dest_path first (for move/rename operations)
        if hasattr(event, "dest_path") and event.dest_path and not is_temp_file(event.dest_path):
            return event.dest_path
        # Then check regular path
        if not is_temp_file(event.path):
            return event.path

    # If all files are temp files, try to extract the base name
    for event in events:
        if hasattr(event, "dest_path") and event.dest_path:
            base_name = extract_base_name(event.dest_path)
            if base_name:
                # Try to construct real path from base name
                real_path = event.dest_path.parent / base_name
                if real_path != event.dest_path:
                    return real_path

        base_name = extract_base_name(event.path)
        if base_name:
            real_path = event.path.parent / base_name
            if real_path == event.path:
                return real_path

    return None

x_find_real_file_from_events__mutmut_mutants : ClassVar[MutantDict] = {
'x_find_real_file_from_events__mutmut_1': x_find_real_file_from_events__mutmut_1, 
    'x_find_real_file_from_events__mutmut_2': x_find_real_file_from_events__mutmut_2, 
    'x_find_real_file_from_events__mutmut_3': x_find_real_file_from_events__mutmut_3, 
    'x_find_real_file_from_events__mutmut_4': x_find_real_file_from_events__mutmut_4, 
    'x_find_real_file_from_events__mutmut_5': x_find_real_file_from_events__mutmut_5, 
    'x_find_real_file_from_events__mutmut_6': x_find_real_file_from_events__mutmut_6, 
    'x_find_real_file_from_events__mutmut_7': x_find_real_file_from_events__mutmut_7, 
    'x_find_real_file_from_events__mutmut_8': x_find_real_file_from_events__mutmut_8, 
    'x_find_real_file_from_events__mutmut_9': x_find_real_file_from_events__mutmut_9, 
    'x_find_real_file_from_events__mutmut_10': x_find_real_file_from_events__mutmut_10, 
    'x_find_real_file_from_events__mutmut_11': x_find_real_file_from_events__mutmut_11, 
    'x_find_real_file_from_events__mutmut_12': x_find_real_file_from_events__mutmut_12, 
    'x_find_real_file_from_events__mutmut_13': x_find_real_file_from_events__mutmut_13, 
    'x_find_real_file_from_events__mutmut_14': x_find_real_file_from_events__mutmut_14, 
    'x_find_real_file_from_events__mutmut_15': x_find_real_file_from_events__mutmut_15, 
    'x_find_real_file_from_events__mutmut_16': x_find_real_file_from_events__mutmut_16, 
    'x_find_real_file_from_events__mutmut_17': x_find_real_file_from_events__mutmut_17, 
    'x_find_real_file_from_events__mutmut_18': x_find_real_file_from_events__mutmut_18, 
    'x_find_real_file_from_events__mutmut_19': x_find_real_file_from_events__mutmut_19, 
    'x_find_real_file_from_events__mutmut_20': x_find_real_file_from_events__mutmut_20, 
    'x_find_real_file_from_events__mutmut_21': x_find_real_file_from_events__mutmut_21, 
    'x_find_real_file_from_events__mutmut_22': x_find_real_file_from_events__mutmut_22, 
    'x_find_real_file_from_events__mutmut_23': x_find_real_file_from_events__mutmut_23, 
    'x_find_real_file_from_events__mutmut_24': x_find_real_file_from_events__mutmut_24, 
    'x_find_real_file_from_events__mutmut_25': x_find_real_file_from_events__mutmut_25, 
    'x_find_real_file_from_events__mutmut_26': x_find_real_file_from_events__mutmut_26, 
    'x_find_real_file_from_events__mutmut_27': x_find_real_file_from_events__mutmut_27, 
    'x_find_real_file_from_events__mutmut_28': x_find_real_file_from_events__mutmut_28, 
    'x_find_real_file_from_events__mutmut_29': x_find_real_file_from_events__mutmut_29, 
    'x_find_real_file_from_events__mutmut_30': x_find_real_file_from_events__mutmut_30
}

def find_real_file_from_events(*args, **kwargs):
    result = _mutmut_trampoline(x_find_real_file_from_events__mutmut_orig, x_find_real_file_from_events__mutmut_mutants, args, kwargs)
    return result 

find_real_file_from_events.__signature__ = _mutmut_signature(x_find_real_file_from_events__mutmut_orig)
x_find_real_file_from_events__mutmut_orig.__name__ = 'x_find_real_file_from_events'


# <3 🧱🤝📄🪄
