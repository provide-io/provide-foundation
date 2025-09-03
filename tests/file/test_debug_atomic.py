"""Debug atomic_write behavior."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from provide.foundation.file.atomic import atomic_write


def test_debug_atomic_write_with_preserve_false():
    """Debug atomic_write with preserve_mode=False."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        path = td / "test.txt"
        path.write_bytes(b"Original")
        os.chmod(path, 0o600)
        print(f"Original file mode: {oct(path.stat().st_mode & 0o777)}")
        print(f"File exists before atomic_write: {path.exists()}")
        
        # Patch os.chmod to see if it's called
        original_chmod = os.chmod
        chmod_calls = []
        
        def tracked_chmod(path, mode):
            chmod_calls.append((str(path), oct(mode)))
            print(f"os.chmod called: {path} -> {oct(mode)}")
            return original_chmod(path, mode)
        
        with patch('os.chmod', side_effect=tracked_chmod):
            atomic_write(path, b"New content", preserve_mode=False)
        
        print(f"chmod was called {len(chmod_calls)} times")
        for call in chmod_calls:
            print(f"  {call}")
        
        print(f"Final file mode: {oct(path.stat().st_mode & 0o777)}")


if __name__ == "__main__":
    test_debug_atomic_write_with_preserve_false()