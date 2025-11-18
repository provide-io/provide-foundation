# provide-testkit Improvements Needed

**Generated:** 2025-11-17
**Source:** Security scanner testing in provide-foundation

## Issues Found

### 1. Excessive Noise in SecurityScanner Output

**Priority:** HIGH
**Effort:** LOW

**Problem:**
The SecurityScanner outputs many informational messages that clutter the actual security findings:

```
nosec encountered (B110), but no failed test on line 230
nosec encountered (B110), but no failed test on line 278
Test in comment: Test is not a test name or id, ignoring
Test in comment: data is not a test name or id, ignoring
... (hundreds of these lines)
```

**Impact:**
- Hard to read actual security findings
- Users may miss real issues in the noise
- Poor user experience

**Solution:**
1. Move "nosec encountered" messages to DEBUG level or suppress entirely
2. Move "Test in comment" warnings to DEBUG level
3. Only show warnings/errors in default output
4. Add verbosity control: `scanner.analyze(path, verbosity='quiet'|'normal'|'verbose')`

**Location:** `provide.testkit.quality.security.scanner`

---

### 2. Path Handling Bug in Result Formatting

**Priority:** MEDIUM
**Effort:** MEDIUM

**Problem:**
Scanner crashes when trying to format relative paths in results:

```python
ValueError: 'src/provide/foundation/concurrency/async_locks.py' is not in the
subpath of '/home/user/provide-foundation' OR one path is relative and the
other is absolute.
```

**Impact:**
- Cannot generate detailed issue reports
- Breaks automated tooling that depends on formatted output

**Solution:**
1. Normalize all paths to absolute before storing in results
2. Convert to relative when displaying, with proper error handling
3. Add tests for path handling edge cases

**Location:** `provide.testkit.quality.security.scanner` result formatting

---

### 3. No Verbosity Control

**Priority:** MEDIUM
**Effort:** LOW

**Problem:**
No way to control output verbosity. Scanner always outputs all messages.

**Impact:**
- Noisy CI/CD pipelines
- Hard to use in automated contexts
- Can't suppress info-level messages

**Solution:**
Add verbosity parameter to SecurityScanner:

```python
scanner = SecurityScanner(config={'verbosity': 'quiet'})
# or
result = scanner.analyze(path, verbosity='quiet')
```

Levels:
- `'quiet'` - Errors only
- `'normal'` - Errors and warnings (default)
- `'verbose'` - All messages including info

**Location:** `provide.testkit.quality.security.scanner.SecurityScanner.__init__`

---

### 4. Insufficient Documentation

**Priority:** LOW
**Effort:** MEDIUM

**Problem:**
SecurityScanner behavior not well documented:
- What constitutes a "failure" vs "warning"
- How to interpret the security score
- What the output messages mean
- How to configure the scanner

**Impact:**
- Users don't know how to use it effectively
- Unclear what to do with scan results
- No best practices guidance

**Solution:**
Add comprehensive documentation:
1. Module-level docstring explaining scanner purpose
2. Document all configuration options
3. Add usage examples (simple, intermediate, advanced)
4. Document score calculation
5. Add interpretation guide for results

**Location:** `provide.testkit.quality.security` module

---

## Summary

| Issue | Priority | Effort | Status |
|-------|----------|--------|--------|
| Excessive noise in output | HIGH | LOW | Open |
| Path handling bug | MEDIUM | MEDIUM | Open |
| No verbosity control | MEDIUM | LOW | Open |
| Insufficient documentation | LOW | MEDIUM | Open |

## Testing Recommendations

After fixes, verify with:
1. Run scanner on provide-foundation codebase
2. Verify output is clean and readable
3. Test with various verbosity levels
4. Verify path formatting works on all platforms
5. Add integration tests for scanner
