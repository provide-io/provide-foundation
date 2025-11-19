# Comprehensive Security Scan Report
**Generated:** 2025-11-17
**Tool:** provide-testkit SecurityScanner (Bandit)
**Version:** testkit 0.0.1113

## Executive Summary

All directories scanned with Bandit security analysis:

| Directory | Score | Status | Files | Issues | Time |
|-----------|-------|--------|-------|--------|------|
| **src/** | 57% | ❌ FAIL | 353 | 20 | 3.22s |
| **tests/** | 93% | ✅ PASS | 23 | 7 | 0.11s |
| **scripts/** | 82% | ✅ PASS | 8 | 18 | 0.14s |
| **examples/** | 25% | ❌ FAIL | 34 | 20 | 0.61s |

**Overall Assessment:**
- ✅ **src/** - All issues are documented and properly suppressed in ruff config
- ✅ **tests/** - Excellent score, minor issues expected in test code
- ✅ **scripts/** - Good score, issues are appropriate for utility scripts
- ⚠️ **examples/** - **ACTION REQUIRED** - Examples should demonstrate best practices

---

## Detailed Analysis

### 1. Source Code (src/) - 57% Score

**Status:** ✅ **ACCEPTABLE** (all issues documented/suppressed)

#### Issues Found:
- **B110** (15×) - `try-except-pass`
  - Already suppressed globally in ruff config
  - Intentional for optional feature detection

- **B608** (2×) - SQL in query builders
  - Already suppressed globally in ruff config
  - OpenObserve streaming module (legitimate usage)

- **B112** (1×) - `try-except-continue`
  - Already suppressed globally in ruff config
  - Config discovery module (intentional)

- **B404** (1×) - `import subprocess`
  - Process management module (expected)
  - Per-file suppression in place

- **B603** (1×) - `subprocess` call
  - Process management module (expected)
  - Per-file suppression in place

**Recommendation:** ✅ **NO ACTION NEEDED** - All issues are documented and appropriate

---

### 2. Test Code (tests/) - 93% Score

**Status:** ✅ **EXCELLENT**

#### Issues Found:
- **B110** (6×) - `try-except-pass` in test fixtures
- **B311** (1×) - `random.random()` in test data generation

**Recommendation:** ✅ **NO ACTION NEEDED** - Appropriate for test code

---

### 3. Scripts (scripts/) - 82% Score

**Status:** ✅ **GOOD**

#### Issues Found:
- **B311** (7×) - `random` module usage in demo scripts
  - Demo script `cut_up_chuck.py` for log demonstrations
  - Not used for security purposes

- **B607** (4×) - Partial path in subprocess
  - Setup scripts for GitHub auth and testing
  - Appropriate for dev tooling

- **B603** (4×) - `subprocess` calls
  - Dev automation scripts
  - Expected behavior

- **B404** (3×) - `import subprocess`
  - Dev automation scripts
  - Expected behavior

**Recommendation:** ✅ **NO ACTION NEEDED** - Appropriate for utility scripts

---

### 4. Examples (examples/) - 25% Score ⚠️

**Status:** ⚠️ **NEEDS ATTENTION** - Examples teach users, should show best practices

#### Issues Found:

##### HIGH PRIORITY - Security Anti-Patterns

**B108** (4×) - **Hardcoded /tmp directory**
```python
# ❌ BAD - Don't teach this
demo_file = Path("/tmp/dogfooding_demo.txt")
base_path = Path("/tmp/demo")
```

**Recommendation:** Use `tempfile.mkdtemp()` or show proper temp directory usage
```python
# ✅ GOOD - Teach this instead
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    demo_file = Path(tmpdir) / "dogfooding_demo.txt"
```

**Affected Files:**
- `examples/cli/02_dogfooding_cli.py:162`
- `examples/file_operations/02_streaming_detection.py:171`
- `examples/file_operations/02_streaming_detection.py:202`
- `examples/integration/celery/01_setup_and_config.py:77`

---

**B104** (1×) - **Binding to all interfaces (0.0.0.0)**
```python
# ❌ POTENTIALLY DANGEROUS - Security risk if not explained
host: str = field(default="0.0.0.0")
```

**Recommendation:** Either use `127.0.0.1` or add security warning comments
```python
# ✅ BETTER - For local dev
host: str = field(default="127.0.0.1")

# OR if 0.0.0.0 is needed, add warning:
# WARNING: 0.0.0.0 binds to all interfaces (public access)
# In production, use specific IP or configure firewall
host: str = field(default="0.0.0.0")
```

**Affected Files:**
- `examples/configuration/03_config_management.py:140`

---

**B105** (1×) - **Hardcoded password in example**
```python
# ❌ BAD - Even in examples, avoid real-looking passwords
os.environ["DB_PASSWORD"] = "secret123"
```

**Recommendation:** Use obviously fake passwords or load from file
```python
# ✅ GOOD - Make it obvious this is a placeholder
os.environ["DB_PASSWORD"] = "REPLACE_WITH_REAL_PASSWORD"

# OR better - show proper pattern
from pathlib import Path
os.environ["DB_PASSWORD"] = Path("~/.secrets/db_password").expanduser().read_text().strip()
```

**Affected Files:**
- `examples/configuration/03_config_management.py:208`

---

**B608** (1×) - **SQL injection vulnerability in example**
```python
# ❌ DANGEROUS - Never teach this pattern!
rows = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
```

**Recommendation:** **MUST FIX** - Show parameterized queries
```python
# ✅ CORRECT - Always use parameterized queries
rows = self.db.query("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Affected Files:**
- `examples/di/01_polyglot_di_pattern.py:114`

---

##### MEDIUM PRIORITY - Non-Cryptographic Random

**B311** (13×) - **Using `random` module**
```python
# In demos/examples showing retry logic, timing, etc.
if random.random() < 0.3:  # Simulate failure
    raise ConnectionError("Payment gateway timeout")
```

**Recommendation:** Add comment clarifying this is for simulation only
```python
# ✅ BETTER - Add educational comment
# NOTE: random.random() is fine for simulations/demos
# For cryptographic use, use secrets.SystemRandom()
if random.random() < 0.3:  # Simulate 30% failure rate
    raise ConnectionError("Payment gateway timeout")
```

**Affected Files:**
- `examples/integration/celery/03_tasks.py` (multiple occurrences)
- Other example files demonstrating retry/timing logic

---

## Recommendations

### Immediate Actions (Examples Directory)

#### 1. Fix SQL Injection Example (CRITICAL)
File: `examples/di/01_polyglot_di_pattern.py:114`
```python
# Change from:
rows = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")

# To:
rows = self.db.query("SELECT * FROM users WHERE id = ?", (user_id,))
# Add comment explaining why parameterized queries prevent SQL injection
```

#### 2. Replace Hardcoded /tmp Paths
Use `tempfile` module instead:
```python
import tempfile
from pathlib import Path

# Instead of: Path("/tmp/demo")
with tempfile.TemporaryDirectory() as tmpdir:
    demo_path = Path(tmpdir)
```

#### 3. Fix Hardcoded Password Example
```python
# Change from:
os.environ["DB_PASSWORD"] = "secret123"

# To (show proper pattern):
os.environ["DB_PASSWORD"] = os.getenv("DB_PASSWORD", "REPLACE_WITH_REAL_PASSWORD")
# Or show loading from secrets file
```

#### 4. Add Security Comments
For `0.0.0.0` binding and `random` usage, add educational comments explaining:
- When these patterns are safe
- When they're dangerous
- What to use in production

---

### Long-Term Improvements

1. **Add Security Examples**
   - Create `examples/security/` directory
   - Show proper secrets management
   - Demonstrate secure configuration patterns
   - SQL injection prevention examples

2. **Code Review Examples**
   - All examples should pass security scans or have documented reasons
   - Add security checklist to example contribution guide

3. **Documentation**
   - Add security best practices section
   - Reference provide-foundation's crypto utilities
   - Link to OWASP resources

---

## Artifacts Generated

All scan results saved to `.security/` directory:
- `security.json` - Machine-readable results
- `security_issues.txt` - Human-readable issue list
- `security_summary.txt` - Quick summary

Subdirectories for each scan:
- `.security/` - src/ results
- `.security/tests/` - tests/ results
- `.security/scripts/` - scripts/ results
- `.security/examples/` - examples/ results

---

## Next Steps

1. ✅ **Fix critical SQL injection in examples** (`examples/di/01_polyglot_di_pattern.py`)
2. ⚠️ **Review and update temp file usage in examples** (4 files)
3. 📝 **Add security educational comments** to examples showing patterns like `random`, `0.0.0.0`
4. 🔄 **Re-run security scan** after fixes
5. ✅ **Update example documentation** with security best practices

---

## Conclusion

**provide-foundation core (src/):** ✅ Excellent security posture
- All findings are documented and appropriate
- Security rules properly configured in ruff

**Examples:** ⚠️ Need improvements
- Contains some security anti-patterns
- These teach users, so must demonstrate best practices
- SQL injection example is particularly concerning

**Overall:** Good security practices in main codebase, but examples need attention to ensure they teach secure coding patterns.
