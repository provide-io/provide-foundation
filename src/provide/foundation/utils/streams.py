"""Stream utilities for foundation library."""

import io
import sys
from typing import TextIO


def get_safe_stderr() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.
    
    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).
    
    Returns:
        A writable text stream, either sys.stderr or io.StringIO()
    """
    return (
        sys.stderr
        if hasattr(sys, "stderr") and sys.stderr is not None
        else io.StringIO()
    )