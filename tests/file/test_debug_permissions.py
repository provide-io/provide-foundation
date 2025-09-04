"""Debug test for permissions."""

import os
import tempfile
from pathlib import Path


def test_debug_atomic_write():
    """Debug what's happening with atomic_write."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        path = td / "test.txt"
        path.write_bytes(b"Original")
        os.chmod(path, 0o600)
        print(f"Original file mode: {oct(path.stat().st_mode & 0o777)}")
        
        # Create temp file like atomic_write does
        temp_path = td / "temp.txt"
        temp_path.write_bytes(b"New content")
        print(f"Temp file mode before any chmod: {oct(temp_path.stat().st_mode & 0o777)}")
        
        # What happens if we DON'T chmod the temp file?
        os.replace(temp_path, path)
        print(f"Final file mode (no chmod): {oct(path.stat().st_mode & 0o777)}")
        
        # Reset
        path.write_bytes(b"Original")
        os.chmod(path, 0o600)
        
        # Now with chmod
        temp_path2 = td / "temp2.txt"
        temp_path2.write_bytes(b"New content 2")
        os.chmod(temp_path2, 0o600)  # Explicitly set to match
        print(f"Temp file mode after chmod: {oct(temp_path2.stat().st_mode & 0o777)}")
        
        os.replace(temp_path2, path)
        print(f"Final file mode (with chmod): {oct(path.stat().st_mode & 0o777)}")


if __name__ == "__main__":
    test_debug_atomic_write()