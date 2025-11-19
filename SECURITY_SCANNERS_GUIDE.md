# Security Scanners Guide

Comprehensive guide for using provide-testkit security scanners across the provide-io ecosystem.

## Overview

provide-testkit includes production-ready security scanners that integrate seamlessly with CI/CD pipelines. All scanners follow a consistent plugin architecture and return standardized `QualityResult` objects.

**Available Scanners:**
- **GitLeaks** - Secret detection (API keys, tokens, credentials)
- **PipAudit** - PyPI package vulnerability scanning
- **Safety** - PyUp vulnerability database scanning
- **Semgrep** - Pattern-based SAST (Static Application Security Testing)
- **SecurityScanner (Bandit)** - Python-specific SAST
- **TruffleHog** - Deep secret detection with verification

**Test Coverage:** 88% overall (all scanners 85-95% coverage)

## Quick Start

### Installation

```bash
# Basic installation
pip install provide-testkit

# With all security scanners (requires Go binaries for GitLeaks/TruffleHog)
pip install bandit semgrep safety pip-audit

# Install GitLeaks (macOS)
brew install gitleaks

# Install TruffleHog (macOS)
brew install trufflehog
```

### Basic Usage

```python
from pathlib import Path
from provide.testkit.quality.security import (
    GitLeaksScanner,
    PipAuditScanner,
    SafetyScanner,
    SemgrepScanner,
    SecurityScanner,
    TruffleHogScanner,
)

# Scan for secrets
gitleaks = GitLeaksScanner(config={"max_secrets": 0})
result = gitleaks.analyze(Path("./src"))
print(f"Secrets found: {result.details['total_secrets']}")
print(f"Score: {result.score}%")
print(f"Passed: {result.passed}")

# Scan Python dependencies for vulnerabilities
pip_audit = PipAuditScanner(config={"max_vulnerabilities": 0})
result = pip_audit.analyze(Path("."))
print(f"Vulnerabilities: {result.details['total_vulnerabilities']}")

# Scan Python code for security issues
bandit = SecurityScanner(config={
    "max_high_severity": 0,
    "max_medium_severity": 5,
    "min_score": 80.0,
    "verbosity": "quiet",  # quiet, normal, or verbose
})
result = bandit.analyze(Path("./src"))
print(f"Issues: {result.details['total_issues']}")
```

## Scanner Details

### 1. GitLeaks - Secret Detection

Scans for exposed secrets like API keys, passwords, and tokens in code and git history.

**Configuration:**
```python
config = {
    "max_secrets": 0,                    # Maximum allowed secrets
    "config_file": ".gitleaks.toml",    # Custom config file
    "verbose": True,                     # Verbose output
    "redact": True,                      # Redact secrets in output
    "timeout": 300,                      # Timeout in seconds
}

scanner = GitLeaksScanner(config)
result = scanner.analyze(Path("./src"), artifact_dir=Path(".security"))
```

**Auto-detection:** Automatically uses `.provide/security/gitleaks.toml` if present.

**Score Calculation:** 100 - (secrets_found × 25)

**Example Output:**
```python
{
    "tool": "gitleaks",
    "passed": False,
    "score": 75.0,
    "details": {
        "total_secrets": 1,
        "secrets": [{
            "description": "AWS Access Key",
            "file": "config.py",
            "line": 10,
            "secret": "***REDACTED***",  # Always redacted
            "rule_id": "aws-access-key",
        }]
    }
}
```

### 2. PipAudit - PyPI Vulnerability Scanner

Scans Python dependencies against the PyPI security advisory database.

**Configuration:**
```python
config = {
    "max_vulnerabilities": 0,           # Maximum allowed vulnerabilities
    "strict": False,                    # Strict mode
    "local": False,                     # Only scan local packages
    "skip_editable": False,             # Skip editable installs
    "timeout": 300,
}

scanner = PipAuditScanner(config)
result = scanner.analyze(Path("."))  # Scans requirements.txt or pyproject.toml
```

**Score Calculation:** 100 - (vulnerabilities × 10)

**Example Output:**
```python
{
    "tool": "pip-audit",
    "passed": False,
    "score": 90.0,
    "details": {
        "total_dependencies": 50,
        "total_vulnerabilities": 1,
        "vulnerabilities": [{
            "package": "requests",
            "version": "2.28.0",
            "id": "PYSEC-2023-123",
            "description": "Request smuggling vulnerability",
            "fix_versions": ["2.31.0"],
        }]
    }
}
```

### 3. Safety - PyUp Vulnerability Database

Scans Python dependencies against the PyUp Safety database.

**Configuration:**
```python
config = {
    "max_vulnerabilities": 0,
    "policy_file": ".safety-policy.yml",  # Policy file path
    "full_report": False,                 # Full vulnerability details
    "ignore_vulns": ["12345", "67890"],  # Vulnerability IDs to ignore
    "timeout": 120,
}

scanner = SafetyScanner(config)
result = scanner.analyze(Path("."))
```

**Auto-detection:** Automatically uses `.provide/security/safety-policy.yml` if present.

**Score Calculation:** 100 - (vulnerabilities × 10)

### 4. Semgrep - Pattern-Based SAST

Scans code for security vulnerabilities, bugs, and anti-patterns using pattern rules.

**Configuration:**
```python
config = {
    "config": ["auto"],                  # or ["p/security-audit", "p/owasp-top-10"]
    "severity": ["ERROR", "WARNING"],    # Severity levels to include
    "max_findings": 0,                   # Maximum allowed findings
    "exclude": ["**/test_*", "**/.venv/**"],
    "max_memory": 4000,                  # Max memory in MB
    "timeout_per_rule": 30,              # Timeout per rule
    "timeout": 600,
}

scanner = SemgrepScanner(config)
result = scanner.analyze(Path("./src"))
```

**Auto-detection:** Automatically uses `.provide/security/semgrep.yml` if present.

**Score Calculation:**
- ERROR: -15 points
- WARNING: -5 points
- INFO: -1 point

**Example Output:**
```python
{
    "tool": "semgrep",
    "passed": True,
    "score": 84.0,
    "details": {
        "total_findings": 3,
        "severity_breakdown": {"ERROR": 1, "WARNING": 1, "INFO": 1},
        "findings": [{
            "check_id": "python.lang.security.audit.exec-used",
            "path": "utils.py",
            "start_line": 42,
            "severity": "ERROR",
            "message": "Use of exec() is dangerous",
        }]
    }
}
```

### 5. SecurityScanner (Bandit) - Python SAST

Scans Python code for common security issues using Bandit.

**Configuration:**
```python
config = {
    "max_high_severity": 0,              # Maximum HIGH severity issues
    "max_medium_severity": 5,            # Maximum MEDIUM severity issues
    "min_score": 80.0,                   # Minimum passing score
    "verbosity": "quiet",                # quiet, normal, or verbose
    "exclude": ["*/tests/*", "*/.venv/*"],  # Exclude patterns
}

scanner = SecurityScanner(config)
result = scanner.analyze(Path("./src"), artifact_dir=Path(".provide/output/security"))
```

**Verbosity Levels:**
- `quiet`: Only errors (best for CI/CD)
- `normal`: Errors and warnings (default)
- `verbose`: All messages including debug info

**Score Calculation:**
- HIGH severity: -10 points
- MEDIUM severity: -5 points
- LOW severity: -1 point

**Example Output:**
```python
{
    "tool": "security",
    "passed": False,
    "score": 90.0,
    "details": {
        "total_files": 25,
        "total_issues": 1,
        "severity_breakdown": {"HIGH": 1, "MEDIUM": 0, "LOW": 0},
        "confidence_breakdown": {"HIGH": 1, "MEDIUM": 0, "LOW": 0},
        "thresholds": {
            "max_high_severity": 0,
            "max_medium_severity": 5,
            "min_score": 80.0,
        },
        "issues": [{
            "filename": "/path/to/file.py",
            "line_number": 42,
            "test_id": "B101",
            "test_name": "assert_used",
            "severity": "HIGH",
            "confidence": "HIGH",
            "text": "Use of assert detected",
            "code": "assert user.is_authenticated",
        }]
    }
}
```

### 6. TruffleHog - Deep Secret Detection

Scans for secrets using entropy analysis and pattern matching with optional verification.

**Configuration:**
```python
config = {
    "max_secrets": 0,
    "only_verified": False,              # Only report verified secrets
    "no_verification": False,            # Skip verification entirely
    "concurrency": 4,                    # Parallel workers
    "include_detectors": ["aws", "github"],  # Only these detectors
    "exclude_detectors": ["generic"],    # Exclude these detectors
    "exclude_paths": ["*.test", "vendor/*"],  # Exclude file patterns
    "timeout": 600,
}

scanner = TruffleHogScanner(config)
result = scanner.analyze(Path("."))
```

**Auto-detection:** Automatically uses `.provide/security/trufflehog.yml` if present.

**Score Calculation:**
- Verified (active) secrets: -50 points each
- Unverified secrets: -15 points each

**Example Output:**
```python
{
    "tool": "trufflehog",
    "passed": False,
    "score": 50.0,
    "details": {
        "total_secrets": 2,
        "verified_secrets": 1,           # 🔴 ACTIVE and dangerous!
        "unverified_secrets": 1,         # ⚪ Potential false positive
        "secrets": [{
            "detector_type": "AWS",
            "detector_name": "AWS Access Key",
            "verified": True,            # Secret is ACTIVE
            "file": "config.py",
            "line": 10,
            "raw": "***REDACTED***",     # Never exposed
            "redacted": "AKIA****************",
        }]
    }
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for GitLeaks

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install scanners
        run: |
          pip install provide-testkit bandit semgrep safety pip-audit
          # Install GitLeaks
          wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
          tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
          sudo mv gitleaks /usr/local/bin/

      - name: Run security scans
        run: |
          python -c "
          from pathlib import Path
          from provide.testkit.quality.security import *

          # Run all scanners
          scanners = [
              ('GitLeaks', GitLeaksScanner({'max_secrets': 0})),
              ('PipAudit', PipAuditScanner({'max_vulnerabilities': 0})),
              ('Safety', SafetyScanner({'max_vulnerabilities': 0})),
              ('Semgrep', SemgrepScanner({'max_findings': 10})),
              ('Bandit', SecurityScanner({'max_high_severity': 0, 'verbosity': 'quiet'})),
          ]

          failed = []
          for name, scanner in scanners:
              result = scanner.analyze(Path('.'))
              print(f'{name}: Score={result.score}%, Passed={result.passed}')
              if not result.passed:
                  failed.append(name)

          if failed:
              print(f'❌ Failed scanners: {failed}')
              exit(1)
          print('✅ All security scans passed!')
          "
```

## Best Practices

### 1. Progressive Security Gates

Start permissive, tighten over time:

```python
# Week 1: Establish baseline
config_baseline = {
    "max_high_severity": 10,
    "max_medium_severity": 50,
    "min_score": 50.0,
}

# Week 4: Tighten requirements
config_strict = {
    "max_high_severity": 5,
    "max_medium_severity": 20,
    "min_score": 70.0,
}

# Production: Zero tolerance
config_production = {
    "max_high_severity": 0,
    "max_medium_severity": 5,
    "min_score": 90.0,
}
```

### 2. Layered Defense

Use multiple scanners for comprehensive coverage:

```python
# Secrets: GitLeaks (fast) + TruffleHog (deep)
# Dependencies: PipAudit + Safety (different databases)
# Code: Bandit (Python-specific) + Semgrep (multi-language)
```

### 3. Artifact Management

Always save artifacts for audit trails:

```python
from datetime import datetime

artifact_dir = Path(f".provide/output/security/{datetime.now().isoformat()}")

for scanner in all_scanners:
    result = scanner.analyze(path, artifact_dir=artifact_dir)
    # Artifacts saved with timestamps for historical tracking
```

### 4. Quiet Mode in CI/CD

Reduce noise in CI/CD logs:

```python
# Bandit verbosity
bandit = SecurityScanner({"verbosity": "quiet"})

# GitLeaks verbose mode off
gitleaks = GitLeaksScanner({"verbose": False})
```

## Troubleshooting

### Scanner Not Available

```python
from provide.testkit.quality.security import (
    GITLEAKS_AVAILABLE,
    PIP_AUDIT_AVAILABLE,
    SAFETY_AVAILABLE,
    SEMGREP_AVAILABLE,
    TRUFFLEHOG_AVAILABLE,
)

if not GITLEAKS_AVAILABLE:
    print("GitLeaks not installed!")
    print("Install: brew install gitleaks")
```

### Timeouts

```python
# Increase timeout for large codebases
scanner = SemgrepScanner({"timeout": 1200})  # 20 minutes
```

### False Positives

```python
# GitLeaks: Use .gitleaksignore
# Semgrep: Use --exclude patterns
# Bandit: Use # nosec comments (sparingly!)
# Safety: Use ignore_vulns list
```

## License

Apache-2.0

## Support

- Documentation: https://github.com/provide-io/provide-testkit
- Issues: https://github.com/provide-io/provide-testkit/issues
- provide-io ecosystem: https://provide.io
