"""
Default values for file operations.
All defaults are defined here instead of inline in function definitions.
"""

# =================================
# Temporary file/directory defaults
# =================================
DEFAULT_TEMP_PREFIX = "provide_"
DEFAULT_TEMP_SUFFIX = ""
DEFAULT_TEMP_CLEANUP = True
DEFAULT_TEMP_TEXT_MODE = False

# =================================
# Directory operation defaults
# =================================
DEFAULT_DIR_MODE = 0o755
DEFAULT_DIR_PARENTS = True
DEFAULT_MISSING_OK = True

# =================================
# Atomic write defaults
# =================================
DEFAULT_ATOMIC_MODE = 0o644
DEFAULT_ATOMIC_ENCODING = "utf-8"