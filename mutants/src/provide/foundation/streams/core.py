# provide/foundation/streams/core.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# core.py
#
import sys
import threading
from typing import TextIO

from provide.foundation.concurrency.locks import get_lock_manager

"""Core stream management for Foundation.
Handles log streams, file handles, and output configuration.
"""

_PROVIDE_LOG_STREAM: TextIO = sys.stderr
_LOG_FILE_HANDLE: TextIO | None = None
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


def x__get_stream_lock__mutmut_orig() -> threading.RLock:
    """Get the stream lock from LockManager.

    Returns managed lock to prevent deadlocks and enable monitoring.
    """
    # Lock is registered during Foundation initialization via register_foundation_locks()
    return get_lock_manager().get_lock("foundation.stream")


def x__get_stream_lock__mutmut_1() -> threading.RLock:
    """Get the stream lock from LockManager.

    Returns managed lock to prevent deadlocks and enable monitoring.
    """
    # Lock is registered during Foundation initialization via register_foundation_locks()
    return get_lock_manager().get_lock(None)


def x__get_stream_lock__mutmut_2() -> threading.RLock:
    """Get the stream lock from LockManager.

    Returns managed lock to prevent deadlocks and enable monitoring.
    """
    # Lock is registered during Foundation initialization via register_foundation_locks()
    return get_lock_manager().get_lock("XXfoundation.streamXX")


def x__get_stream_lock__mutmut_3() -> threading.RLock:
    """Get the stream lock from LockManager.

    Returns managed lock to prevent deadlocks and enable monitoring.
    """
    # Lock is registered during Foundation initialization via register_foundation_locks()
    return get_lock_manager().get_lock("FOUNDATION.STREAM")

x__get_stream_lock__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_stream_lock__mutmut_1': x__get_stream_lock__mutmut_1, 
    'x__get_stream_lock__mutmut_2': x__get_stream_lock__mutmut_2, 
    'x__get_stream_lock__mutmut_3': x__get_stream_lock__mutmut_3
}

def _get_stream_lock(*args, **kwargs):
    result = _mutmut_trampoline(x__get_stream_lock__mutmut_orig, x__get_stream_lock__mutmut_mutants, args, kwargs)
    return result 

_get_stream_lock.__signature__ = _mutmut_signature(x__get_stream_lock__mutmut_orig)
x__get_stream_lock__mutmut_orig.__name__ = 'x__get_stream_lock'


def x_get_log_stream__mutmut_orig() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_1() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_2() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=None):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_3() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=6.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_4() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name") or _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_5() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed") or not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_6() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(None, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_7() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, None)
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_8() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr("closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_9() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, )
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_10() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "XXclosedXX")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_11() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "CLOSED")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_12() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_13() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(None, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_14() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, None)  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_15() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr("_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_16() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, )  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_17() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "XX_mock_nameXX")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_18() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_MOCK_NAME")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_19() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") or sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_20() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(None, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_21() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, None) and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_22() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr("stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_23() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, ) and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_24() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "XXstderrXX") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_25() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "STDERR") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_26() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_27() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_28() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") or sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_29() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(None, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_30() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, None) and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_31() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr("closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_32() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, ) and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_33() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "XXclosedXX") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_34() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "CLOSED") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_35() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = None
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_36() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = None  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_37() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError(None) from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_38() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("XXAll available streams are closedXX") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_39() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("all available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_40() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("ALL AVAILABLE STREAMS ARE CLOSED") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_41() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = None
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_42() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError(None) from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_43() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("XXNo stderr availableXX") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_44() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("no stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_45() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("NO STDERR AVAILABLE") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_46() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        None
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_47() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            None
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_48() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") or sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_49() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(None, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_50() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, None) and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_51() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr("stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_52() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, ) and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_53() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "XXstderrXX") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_54() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "STDERR") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_55() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_56() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_57() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") or sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_58() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(None, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_59() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, None) and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_60() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr("closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_61() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, ) and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_62() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "XXclosedXX") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_63() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "CLOSED") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_64() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = None
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_65() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError(None) from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_66() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("XXAll available streams are closed (including stderr)XX") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_67() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("all available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_68() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("ALL AVAILABLE STREAMS ARE CLOSED (INCLUDING STDERR)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_69() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError(None) from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_70() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("XXStream validation failed - stderr unavailableXX") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_71() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_72() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("STREAM VALIDATION FAILED - STDERR UNAVAILABLE") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_73() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError(None) from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_74() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("XXStream validation failed - no stderr availableXX") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_75() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()


def x_get_log_stream__mutmut_76() -> TextIO:  # noqa: C901
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return sys.stderr
    try:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
                        pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("STREAM VALIDATION FAILED - NO STDERR AVAILABLE") from e

        return _PROVIDE_LOG_STREAM
    finally:
        _get_stream_lock().release()

x_get_log_stream__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_log_stream__mutmut_1': x_get_log_stream__mutmut_1, 
    'x_get_log_stream__mutmut_2': x_get_log_stream__mutmut_2, 
    'x_get_log_stream__mutmut_3': x_get_log_stream__mutmut_3, 
    'x_get_log_stream__mutmut_4': x_get_log_stream__mutmut_4, 
    'x_get_log_stream__mutmut_5': x_get_log_stream__mutmut_5, 
    'x_get_log_stream__mutmut_6': x_get_log_stream__mutmut_6, 
    'x_get_log_stream__mutmut_7': x_get_log_stream__mutmut_7, 
    'x_get_log_stream__mutmut_8': x_get_log_stream__mutmut_8, 
    'x_get_log_stream__mutmut_9': x_get_log_stream__mutmut_9, 
    'x_get_log_stream__mutmut_10': x_get_log_stream__mutmut_10, 
    'x_get_log_stream__mutmut_11': x_get_log_stream__mutmut_11, 
    'x_get_log_stream__mutmut_12': x_get_log_stream__mutmut_12, 
    'x_get_log_stream__mutmut_13': x_get_log_stream__mutmut_13, 
    'x_get_log_stream__mutmut_14': x_get_log_stream__mutmut_14, 
    'x_get_log_stream__mutmut_15': x_get_log_stream__mutmut_15, 
    'x_get_log_stream__mutmut_16': x_get_log_stream__mutmut_16, 
    'x_get_log_stream__mutmut_17': x_get_log_stream__mutmut_17, 
    'x_get_log_stream__mutmut_18': x_get_log_stream__mutmut_18, 
    'x_get_log_stream__mutmut_19': x_get_log_stream__mutmut_19, 
    'x_get_log_stream__mutmut_20': x_get_log_stream__mutmut_20, 
    'x_get_log_stream__mutmut_21': x_get_log_stream__mutmut_21, 
    'x_get_log_stream__mutmut_22': x_get_log_stream__mutmut_22, 
    'x_get_log_stream__mutmut_23': x_get_log_stream__mutmut_23, 
    'x_get_log_stream__mutmut_24': x_get_log_stream__mutmut_24, 
    'x_get_log_stream__mutmut_25': x_get_log_stream__mutmut_25, 
    'x_get_log_stream__mutmut_26': x_get_log_stream__mutmut_26, 
    'x_get_log_stream__mutmut_27': x_get_log_stream__mutmut_27, 
    'x_get_log_stream__mutmut_28': x_get_log_stream__mutmut_28, 
    'x_get_log_stream__mutmut_29': x_get_log_stream__mutmut_29, 
    'x_get_log_stream__mutmut_30': x_get_log_stream__mutmut_30, 
    'x_get_log_stream__mutmut_31': x_get_log_stream__mutmut_31, 
    'x_get_log_stream__mutmut_32': x_get_log_stream__mutmut_32, 
    'x_get_log_stream__mutmut_33': x_get_log_stream__mutmut_33, 
    'x_get_log_stream__mutmut_34': x_get_log_stream__mutmut_34, 
    'x_get_log_stream__mutmut_35': x_get_log_stream__mutmut_35, 
    'x_get_log_stream__mutmut_36': x_get_log_stream__mutmut_36, 
    'x_get_log_stream__mutmut_37': x_get_log_stream__mutmut_37, 
    'x_get_log_stream__mutmut_38': x_get_log_stream__mutmut_38, 
    'x_get_log_stream__mutmut_39': x_get_log_stream__mutmut_39, 
    'x_get_log_stream__mutmut_40': x_get_log_stream__mutmut_40, 
    'x_get_log_stream__mutmut_41': x_get_log_stream__mutmut_41, 
    'x_get_log_stream__mutmut_42': x_get_log_stream__mutmut_42, 
    'x_get_log_stream__mutmut_43': x_get_log_stream__mutmut_43, 
    'x_get_log_stream__mutmut_44': x_get_log_stream__mutmut_44, 
    'x_get_log_stream__mutmut_45': x_get_log_stream__mutmut_45, 
    'x_get_log_stream__mutmut_46': x_get_log_stream__mutmut_46, 
    'x_get_log_stream__mutmut_47': x_get_log_stream__mutmut_47, 
    'x_get_log_stream__mutmut_48': x_get_log_stream__mutmut_48, 
    'x_get_log_stream__mutmut_49': x_get_log_stream__mutmut_49, 
    'x_get_log_stream__mutmut_50': x_get_log_stream__mutmut_50, 
    'x_get_log_stream__mutmut_51': x_get_log_stream__mutmut_51, 
    'x_get_log_stream__mutmut_52': x_get_log_stream__mutmut_52, 
    'x_get_log_stream__mutmut_53': x_get_log_stream__mutmut_53, 
    'x_get_log_stream__mutmut_54': x_get_log_stream__mutmut_54, 
    'x_get_log_stream__mutmut_55': x_get_log_stream__mutmut_55, 
    'x_get_log_stream__mutmut_56': x_get_log_stream__mutmut_56, 
    'x_get_log_stream__mutmut_57': x_get_log_stream__mutmut_57, 
    'x_get_log_stream__mutmut_58': x_get_log_stream__mutmut_58, 
    'x_get_log_stream__mutmut_59': x_get_log_stream__mutmut_59, 
    'x_get_log_stream__mutmut_60': x_get_log_stream__mutmut_60, 
    'x_get_log_stream__mutmut_61': x_get_log_stream__mutmut_61, 
    'x_get_log_stream__mutmut_62': x_get_log_stream__mutmut_62, 
    'x_get_log_stream__mutmut_63': x_get_log_stream__mutmut_63, 
    'x_get_log_stream__mutmut_64': x_get_log_stream__mutmut_64, 
    'x_get_log_stream__mutmut_65': x_get_log_stream__mutmut_65, 
    'x_get_log_stream__mutmut_66': x_get_log_stream__mutmut_66, 
    'x_get_log_stream__mutmut_67': x_get_log_stream__mutmut_67, 
    'x_get_log_stream__mutmut_68': x_get_log_stream__mutmut_68, 
    'x_get_log_stream__mutmut_69': x_get_log_stream__mutmut_69, 
    'x_get_log_stream__mutmut_70': x_get_log_stream__mutmut_70, 
    'x_get_log_stream__mutmut_71': x_get_log_stream__mutmut_71, 
    'x_get_log_stream__mutmut_72': x_get_log_stream__mutmut_72, 
    'x_get_log_stream__mutmut_73': x_get_log_stream__mutmut_73, 
    'x_get_log_stream__mutmut_74': x_get_log_stream__mutmut_74, 
    'x_get_log_stream__mutmut_75': x_get_log_stream__mutmut_75, 
    'x_get_log_stream__mutmut_76': x_get_log_stream__mutmut_76
}

def get_log_stream(*args, **kwargs):
    result = _mutmut_trampoline(x_get_log_stream__mutmut_orig, x_get_log_stream__mutmut_mutants, args, kwargs)
    return result 

get_log_stream.__signature__ = _mutmut_signature(x_get_log_stream__mutmut_orig)
x_get_log_stream__mutmut_orig.__name__ = 'x_get_log_stream'


def x__reconfigure_structlog_stream__mutmut_orig() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_1() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = None
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_2() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config or "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_3() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "XXlogger_factoryXX" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_4() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "LOGGER_FACTORY" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_5() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" not in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_6() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = None
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_7() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = None

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_8() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_9() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = None
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_10() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = None
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_11() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["XXlogger_factoryXX"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_12() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["LOGGER_FACTORY"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_13() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=None)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_14() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = None
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_15() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["XXcache_logger_on_first_useXX"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


def x__reconfigure_structlog_stream__mutmut_16() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["CACHE_LOGGER_ON_FIRST_USE"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass

x__reconfigure_structlog_stream__mutmut_mutants : ClassVar[MutantDict] = {
'x__reconfigure_structlog_stream__mutmut_1': x__reconfigure_structlog_stream__mutmut_1, 
    'x__reconfigure_structlog_stream__mutmut_2': x__reconfigure_structlog_stream__mutmut_2, 
    'x__reconfigure_structlog_stream__mutmut_3': x__reconfigure_structlog_stream__mutmut_3, 
    'x__reconfigure_structlog_stream__mutmut_4': x__reconfigure_structlog_stream__mutmut_4, 
    'x__reconfigure_structlog_stream__mutmut_5': x__reconfigure_structlog_stream__mutmut_5, 
    'x__reconfigure_structlog_stream__mutmut_6': x__reconfigure_structlog_stream__mutmut_6, 
    'x__reconfigure_structlog_stream__mutmut_7': x__reconfigure_structlog_stream__mutmut_7, 
    'x__reconfigure_structlog_stream__mutmut_8': x__reconfigure_structlog_stream__mutmut_8, 
    'x__reconfigure_structlog_stream__mutmut_9': x__reconfigure_structlog_stream__mutmut_9, 
    'x__reconfigure_structlog_stream__mutmut_10': x__reconfigure_structlog_stream__mutmut_10, 
    'x__reconfigure_structlog_stream__mutmut_11': x__reconfigure_structlog_stream__mutmut_11, 
    'x__reconfigure_structlog_stream__mutmut_12': x__reconfigure_structlog_stream__mutmut_12, 
    'x__reconfigure_structlog_stream__mutmut_13': x__reconfigure_structlog_stream__mutmut_13, 
    'x__reconfigure_structlog_stream__mutmut_14': x__reconfigure_structlog_stream__mutmut_14, 
    'x__reconfigure_structlog_stream__mutmut_15': x__reconfigure_structlog_stream__mutmut_15, 
    'x__reconfigure_structlog_stream__mutmut_16': x__reconfigure_structlog_stream__mutmut_16
}

def _reconfigure_structlog_stream(*args, **kwargs):
    result = _mutmut_trampoline(x__reconfigure_structlog_stream__mutmut_orig, x__reconfigure_structlog_stream__mutmut_mutants, args, kwargs)
    return result 

_reconfigure_structlog_stream.__signature__ = _mutmut_signature(x__reconfigure_structlog_stream__mutmut_orig)
x__reconfigure_structlog_stream__mutmut_orig.__name__ = 'x__reconfigure_structlog_stream'


def x_set_log_stream_for_testing__mutmut_orig(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.
    """
    from provide.foundation.testmode.detection import should_allow_stream_redirect

    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        # Use testmode to determine if redirect is allowed
        if not should_allow_stream_redirect():
            return

        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()
    finally:
        _get_stream_lock().release()


def x_set_log_stream_for_testing__mutmut_1(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.
    """
    from provide.foundation.testmode.detection import should_allow_stream_redirect

    global _PROVIDE_LOG_STREAM
    if _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        # Use testmode to determine if redirect is allowed
        if not should_allow_stream_redirect():
            return

        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()
    finally:
        _get_stream_lock().release()


def x_set_log_stream_for_testing__mutmut_2(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.
    """
    from provide.foundation.testmode.detection import should_allow_stream_redirect

    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=None):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        # Use testmode to determine if redirect is allowed
        if not should_allow_stream_redirect():
            return

        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()
    finally:
        _get_stream_lock().release()


def x_set_log_stream_for_testing__mutmut_3(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.
    """
    from provide.foundation.testmode.detection import should_allow_stream_redirect

    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=6.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        # Use testmode to determine if redirect is allowed
        if not should_allow_stream_redirect():
            return

        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()
    finally:
        _get_stream_lock().release()


def x_set_log_stream_for_testing__mutmut_4(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.
    """
    from provide.foundation.testmode.detection import should_allow_stream_redirect

    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        # Use testmode to determine if redirect is allowed
        if should_allow_stream_redirect():
            return

        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()
    finally:
        _get_stream_lock().release()


def x_set_log_stream_for_testing__mutmut_5(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.
    """
    from provide.foundation.testmode.detection import should_allow_stream_redirect

    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        # Use testmode to determine if redirect is allowed
        if not should_allow_stream_redirect():
            return

        _PROVIDE_LOG_STREAM = None

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()
    finally:
        _get_stream_lock().release()


def x_set_log_stream_for_testing__mutmut_6(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.
    """
    from provide.foundation.testmode.detection import should_allow_stream_redirect

    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        # Use testmode to determine if redirect is allowed
        if not should_allow_stream_redirect():
            return

        _PROVIDE_LOG_STREAM = stream if stream is None else sys.stderr

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()
    finally:
        _get_stream_lock().release()

x_set_log_stream_for_testing__mutmut_mutants : ClassVar[MutantDict] = {
'x_set_log_stream_for_testing__mutmut_1': x_set_log_stream_for_testing__mutmut_1, 
    'x_set_log_stream_for_testing__mutmut_2': x_set_log_stream_for_testing__mutmut_2, 
    'x_set_log_stream_for_testing__mutmut_3': x_set_log_stream_for_testing__mutmut_3, 
    'x_set_log_stream_for_testing__mutmut_4': x_set_log_stream_for_testing__mutmut_4, 
    'x_set_log_stream_for_testing__mutmut_5': x_set_log_stream_for_testing__mutmut_5, 
    'x_set_log_stream_for_testing__mutmut_6': x_set_log_stream_for_testing__mutmut_6
}

def set_log_stream_for_testing(*args, **kwargs):
    result = _mutmut_trampoline(x_set_log_stream_for_testing__mutmut_orig, x_set_log_stream_for_testing__mutmut_mutants, args, kwargs)
    return result 

set_log_stream_for_testing.__signature__ = _mutmut_signature(x_set_log_stream_for_testing__mutmut_orig)
x_set_log_stream_for_testing__mutmut_orig.__name__ = 'x_set_log_stream_for_testing'


def x_ensure_stderr_default__mutmut_orig() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
    finally:
        _get_stream_lock().release()


def x_ensure_stderr_default__mutmut_1() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    if _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
    finally:
        _get_stream_lock().release()


def x_ensure_stderr_default__mutmut_2() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=None):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
    finally:
        _get_stream_lock().release()


def x_ensure_stderr_default__mutmut_3() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=6.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
    finally:
        _get_stream_lock().release()


def x_ensure_stderr_default__mutmut_4() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        if _PROVIDE_LOG_STREAM is not sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
    finally:
        _get_stream_lock().release()


def x_ensure_stderr_default__mutmut_5() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = None
    finally:
        _get_stream_lock().release()

x_ensure_stderr_default__mutmut_mutants : ClassVar[MutantDict] = {
'x_ensure_stderr_default__mutmut_1': x_ensure_stderr_default__mutmut_1, 
    'x_ensure_stderr_default__mutmut_2': x_ensure_stderr_default__mutmut_2, 
    'x_ensure_stderr_default__mutmut_3': x_ensure_stderr_default__mutmut_3, 
    'x_ensure_stderr_default__mutmut_4': x_ensure_stderr_default__mutmut_4, 
    'x_ensure_stderr_default__mutmut_5': x_ensure_stderr_default__mutmut_5
}

def ensure_stderr_default(*args, **kwargs):
    result = _mutmut_trampoline(x_ensure_stderr_default__mutmut_orig, x_ensure_stderr_default__mutmut_mutants, args, kwargs)
    return result 

ensure_stderr_default.__signature__ = _mutmut_signature(x_ensure_stderr_default__mutmut_orig)
x_ensure_stderr_default__mutmut_orig.__name__ = 'x_ensure_stderr_default'


# <3 🧱🤝🌊🪄
