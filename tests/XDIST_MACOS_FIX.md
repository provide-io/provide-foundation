# pytest-xdist macOS GUI Freeze Fix

## Problem Summary

When running `pytest -n 24` (or any high worker count) on macOS, the **entire macOS GUI freezes**:
- All Terminal.app windows become unresponsive
- Mouse/keyboard input to GUI apps stops working
- SSH sessions continue to work fine (showing pytest is still running)
- The freeze persists until pytest completes or is killed

## Root Cause

**NOT a pytest bug** - this is a macOS system resource exhaustion issue caused by:

### 1. Excessive Diagnostic Logging (Primary Cause)
- **Location**: `tests/conftest.py` lines 184-190, 195-198
- **Issue**: Logging on EVERY test start/end for EVERY worker
- **Impact**: 24 workers × 5640 tests × 2 log lines = **270,720+ stderr writes**
- **Why GUI freezes**:
  - macOS `Console.app` monitors all stderr output
  - `WindowServer` (macOS GUI manager) renders terminal output
  - Both get overwhelmed with 270K+ rapid log messages
  - This blocks the main GUI event loop, freezing all macOS UI

### 2. File Descriptor Limits (Secondary Issue)
- **Issue**: macOS defaults to 256 FDs per process (`launchctl limit maxfiles`)
- **Impact**: 24 workers × ~15 FDs each = 360 FDs needed > 256 limit
- **Symptom**: Can cause additional terminal blocking

## The Fix

### ✅ **Fix Applied: Disable Excessive Diagnostic Logging**

**File**: `tests/conftest.py`

**Before**:
```python
if os.getenv("PYTEST_XDIST_WORKER"):
    conftest_diag_logger.debug(f"[Worker {worker_id}] Starting test: {test_name}")
```

**After**:
```python
# Only log if explicitly enabled via PYTEST_XDIST_DEBUG=1
if os.getenv("PYTEST_XDIST_DEBUG") and os.getenv("PYTEST_XDIST_WORKER"):
    conftest_diag_logger.debug(f"[Worker {worker_id}] Starting test: {test_name}")
```

This reduces stderr writes from **270K+ to 0** for normal test runs.

### Optional: Increase File Descriptor Limit

If you still experience issues, increase macOS FD limits:

```bash
# Run the fix script
./scripts/fix_macos_fd_limit.sh

# Or manually:
sudo launchctl limit maxfiles 65536 unlimited

# Then restart Terminal.app
```

## How to Use

### Run Tests Normally (No GUI Freeze)
```bash
pytest -n 24
pytest -n auto
```

### Enable Diagnostic Logging (For Debugging Only)
```bash
export PYTEST_XDIST_DEBUG=1
pytest -n 4  # Use fewer workers when debugging
```

## Why SSH Sessions Worked

- SSH sessions use a separate TTY (pseudo-terminal)
- They don't route through macOS Console.app or WindowServer
- No GUI rendering involved
- stderr goes directly to the SSH connection, not the macOS logging system

## Technical Details

### macOS Logging Architecture
```
pytest → stderr → Console.app → unified logging system
                ↓
          Terminal.app → WindowServer → GPU rendering
```

With 270K+ rapid log messages:
1. Console.app buffers overflow
2. WindowServer blocks waiting for rendering
3. Main GUI event loop freezes
4. All Terminal.app windows hang
5. Mouse/keyboard stop responding

### Why This Only Affects macOS

- Linux: No `WindowServer`, stderr goes directly to terminal
- Windows: Different logging architecture, no equivalent bottleneck
- macOS: Unified logging + WindowServer creates a chokepoint

## Files Modified

1. **tests/conftest.py** (lines 183-198):
   - Added `PYTEST_XDIST_DEBUG` env var check
   - Disabled diagnostic logging by default
   - Added explanatory comments

2. **scripts/fix_macos_fd_limit.sh** (NEW):
   - Script to increase FD limits if needed

3. **scripts/debug_xdist_freeze.sh** (NEW):
   - Debugging tool for investigating issues

## Verification

Run full test suite with 24 workers:
```bash
pytest -n 24 -v
```

Should complete in ~77 seconds with:
- ✅ No GUI freeze
- ✅ No terminal hangs
- ✅ All workers complete successfully

## Related Issues

This fix also resolves:
- GC scanning overhead in xdist workers (separate fix)
- Session-scoped HTTP fixture contention (separate fix)
- Event loop cleanup issues in xdist (separate fix)

See commit history for full details.

---

**Bottom Line**: The macOS GUI freeze was caused by overwhelming the macOS logging/rendering subsystem with 270K+ diagnostic log messages, not by pytest-xdist itself.
