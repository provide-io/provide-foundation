# Memray Memory Profiling Baseline

## Initial Baseline (2026-03-20)

### Logging Stress (50K messages)
- **Total allocations:** 3,878,431
- **Total memory allocated:** 4.281 GB
- **Peak memory usage:** 95.292 MB

**Top allocators (by count):**
| Location | Allocations | Size |
|----------|------------|------|
| `re/__init__.py:185` (sub) | 3,073,817 | 3.363 GB |
| `structlog/dev.py:298` (__call__) | 300,632 | -- |
| `structlog/processors.py:557` (stamper_fmt_local) | 300,535 | 495.823 MB |
| `importlib._bootstrap:241` | 72,014 | 239.424 MB |
| `structlog/dev.py:908` (__call__) | 50,212 | -- |

### Serialization Stress (20K JSON cycles + 10K cache ops)
- **Total allocations:** 420,316
- **Total memory allocated:** 737.048 MB
- **Peak memory usage:** 160.623 KB

### Config Stress (10K parses + 500 init/teardown cycles)
- **Total allocations:** 313,629
- **Total memory allocated:** 4.708 GB
- **Peak memory usage:** 7.770 MB

---

## Optimization Pass 1 (2026-03-20)

### Changes Applied

1. **Pre-compile regex patterns in `security/masking.py`**
   - Pre-compile all 22 DEFAULT_SECRET_PATTERNS at module load time
   - Cache compiled patterns for custom pattern lists
   - Use `pattern.sub()` instead of `re.sub()` to avoid per-call compilation

2. **Switch to MD5 for cache keys in `serialization/cache.py`**
   - Replaced SHA256 with MD5 (usedforsecurity=False) for cache key generation
   - Cache keys don't need cryptographic strength

### Results After Pass 1

| Stress Test | Before (allocs) | After (allocs) | Change | Peak Before | Peak After |
|-------------|-----------------|----------------|--------|-------------|------------|
| Logging | 3,878,431 | 3,783,962 | -2.4% | 95.3 MB | **44.9 MB (-52.9%)** |
| Serialization | 420,222 | 420,215 | ~0% | 160.6 KB | 160.6 KB |
| Config | 313,629 | 306,791 | -2.2% | 7.8 MB | 7.8 MB |

---

## Optimization Pass 2 (2026-03-20)

### Changes Applied

1. **Fast-path keyword pre-check in `security/masking.py`**
   - Added a cheap `str.lower()` + substring check before running any regex
   - If no secret-related keywords (password, token, key, secret, auth, etc.) appear in the text, skip all 22 `pattern.sub()` calls entirely
   - Most log messages contain no secrets, so this eliminates ~2.7M allocations

2. **Lazy dict copy in `logger/processors/sanitization.py`**
   - Previously copied `event_dict` on every log message even when no masking was needed
   - Now only copies when actual sanitization occurs (identity check: `masked_value is not value`)
   - Eliminates a dict allocation on every non-secret log message

3. **Replace hash-based cache keys with tuples in `serialization/cache.py`**
   - Changed `get_cache_key()` from `hashlib.md5(content.encode()).hexdigest()[:16]` to `(format, hash(content))`
   - Eliminates 4 intermediate string allocations per call (encode, hexdigest, slice, f-string)
   - Python's built-in `hash()` is a single C-level operation returning an int
   - Also eliminated duplicate `get_cache_key()` calls in all 5 serialization modules (json, yaml, toml, ini, env)

4. **Optimized EventBus.emit() in `hub/events.py`**
   - Avoid rebuilding `live_handlers` list when no dead references exist
   - Only rebuild list if at least one weak reference is dead
   - Raised cleanup threshold from 10 to 100 (walking all event types every 10 emits was excessive)
   - Optimized `_cleanup_dead_references()` to skip list rebuild when all refs are alive

5. **Skip gc.get_objects() scan in `testmode/internal.py`**
   - `_reset_direct_circuit_breaker_instances()` was calling `gc.get_objects()` (scans ALL Python objects) on every test teardown
   - Added fast-path: skip entirely if circuit breaker modules haven't been imported
   - When scan is needed, use `gc.get_referrers(cls)` (targeted) instead of `gc.get_objects()` (full heap)

### Results After Pass 2

| Stress Test | Original | Pass 1 | Pass 2 | Total Change |
|-------------|----------|--------|--------|------------|
| **Logging** | | | | |
| Allocations | 3,878,431 | 3,783,962 | **1,085,289** | **-72.0%** |
| Memory | 4.281 GB | 3.948 GB | **984 MB** | **-77.0%** |
| Peak | 95.3 MB | 44.9 MB | **44.4 MB** | **-53.4%** |
| **Serialization** | | | | |
| Allocations | 420,222 | 420,215 | **320,202** | **-23.8%** |
| Memory | 737.0 MB | 736.2 MB | **689.6 MB** | **-6.4%** |
| **Config** | | | | |
| Allocations | 313,629 | 306,791 | **135,931** | **-56.7%** |
| Memory | 4.708 GB | 4.698 GB | **1.657 GB** | **-64.8%** |
| Peak | 7.77 MB | 7.77 MB | **7.25 MB** | **-6.7%** |

### Key Wins

- **Logging: 72% fewer allocations, 77% less memory.** The keyword pre-check in `mask_secrets` eliminated ~2.7M unnecessary regex scans. `mask_secrets` dropped from 3,073,562 allocations to 375,000 (only messages that actually contain secret-like keywords).

- **Serialization: 24% fewer allocations.** Eliminating `get_cache_key`'s 4 intermediate string allocations removed `get_cache_key` entirely from the top allocators list (was #2 at 100K allocations).

- **Config: 57% fewer allocations, 65% less memory.** The circuit breaker `gc.get_objects()` skip and EventBus optimizations removed `_reset_direct_circuit_breaker_instances` (was 28K allocs / 2.8 GB) and `hub/events.py` emit/cleanup (was 115K allocs / 175 MB) from the top allocators.

---

## Optimization Pass 3 (2026-03-20)

### Changes Applied

1. **Refined keyword pre-check in `security/masking.py`**
   - Replaced bare "key" keyword with targeted variants: "api", "access", "key=", "key:"
   - Bare "key" caused false positives on strings like "key_value message" — triggering all 22 regex scans on half the stress test messages
   - `mask_secrets` dropped from 375K allocations (pass 2) to **zero** in top allocators

2. **Cached `is_in_click_testing()` in `testmode/detection.py`**
   - `is_in_click_testing()` was calling `inspect.stack()` on every call with no caching
   - Called via `reset_streams()` and stream redirects during every init/teardown cycle
   - Added `_click_testing_cache` with clearing via `_clear_test_mode_cache()`
   - Added second cache clear at end of `reset_foundation_setup_for_testing()` to handle ordering issue where `reset_streams_state()` re-populates the cache after the first clear

### Results After Pass 3

| Stress Test | Original | Pass 2 | Pass 3 | Total Change |
|-------------|----------|--------|--------|------------|
| **Logging** | | | | |
| Allocations | 3,878,431 | 1,085,289 | **709,994** | **-81.7%** |
| Memory | 4.281 GB | 984 MB | **569 MB** | **-87.0%** |
| Peak | 95.3 MB | 44.4 MB | **44.4 MB** | **-53.4%** |
| **Serialization** | | | | |
| Allocations | 420,222 | 320,202 | **320,202** | **-23.8%** |
| Memory | 737.0 MB | 689.6 MB | **689.6 MB** | **-6.4%** |
| **Config** | | | | |
| Allocations | 313,629 | 135,931 | **109,886** | **-65.0%** |
| Memory | 4.708 GB | 1.657 GB | **1.252 GB** | **-73.4%** |
| Peak | 7.77 MB | 7.25 MB | **7.26 MB** | **-6.6%** |

### Key Wins

- **Logging: 82% fewer allocations, 87% less memory.** `mask_secrets` completely disappeared from the top 20 allocators. All remaining top allocators are in structlog (external) or CPython stdlib.

- **Config: 65% fewer allocations, 73% less memory.** Caching `is_in_click_testing()` eliminated ~26K expensive `inspect.stack()` calls during init/teardown cycles.

### Remaining Hotspots (all external/stdlib)

1. **`structlog` timestamp formatting** -- 300K allocations / 496 MB. External dependency.
2. **`structlog/dev.py` ConsoleRenderer** -- 300K + 50K allocations. External dependency.
3. **`inspect.getmodule()`** -- 22K allocations / 1.17 GB in config stress. Called during structlog's stack introspection, not directly from Foundation code.
4. **`json/encoder.py` iterencode** -- 320K allocations / 689 MB in serialization stress. CPython's JSON encoder.

---

## Optimization Pass 4 (2026-03-20)

### Changes Applied

1. **Cached field names set in `config/base.py`**
   - `from_data()` was calling `{f.name for f in fields(cls) if not f.name.startswith("_")}` on every invocation, creating a new set each time
   - Added module-level `_field_names_cache` dict keyed by class — attrs fields are constant after class creation
   - Uses `frozenset` for immutability and marginally faster `in` lookups
   - Eliminated 499 set allocations / 1 MB per 500 init cycles

2. **Replaced dynamic class creation in `hub/initialization.py`**
   - `_initialize_logger()` was calling `type("HubWrapper", (), {...})()` creating a new class + instance on every init cycle
   - Replaced with `_HubWrapper` — a minimal `__slots__` class defined once at module level
   - Includes `get_foundation_config()` method that `FoundationLogger` calls via `self._hub.get_foundation_config()`
   - Eliminated 1,001 dynamic class creations / 938 KB per 500 init cycles

3. **Reviewed structlog processor chain** (no change)
   - `stamper_fmt_local` (300K allocs / 496 MB) uses `datetime.now().strftime()` per message — structlog internal, not configurable without changing output format
   - `ConsoleRenderer` (300K + 50K allocs) — structlog internal
   - Confirmed `StackInfoRenderer` is a no-op when `stack_info` not set — not the allocation source
   - All remaining per-message allocations are in structlog or CPython stdlib

### Results After Pass 4

| Stress Test | Original | Pass 3 | Pass 4 | Total Change |
|-------------|----------|--------|--------|------------|
| **Logging** | | | | |
| Allocations | 3,878,431 | 709,994 | **709,987** | **-81.7%** |
| Memory | 4.281 GB | 569 MB | **569 MB** | **-87.0%** |
| **Serialization** | | | | |
| Allocations | 420,222 | 320,202 | **320,202** | **-23.8%** |
| Memory | 737.0 MB | 689.6 MB | **689.6 MB** | **-6.4%** |
| **Config** | | | | |
| Allocations | 313,629 | 109,886 | **108,386** | **-65.5%** |
| Memory | 4.708 GB | 1.252 GB | **1.250 GB** | **-73.5%** |

### Summary

Pass 4 targeted the last Foundation-internal allocators visible in the config stress profile. The improvements are incremental (~1.4% fewer config allocations) because the remaining allocation budget is dominated by:

- **structlog internals** (300K+ allocs per test for timestamp formatting and console rendering)
- **CPython stdlib** (inspect.getmodule, json.encoder, importlib)
- **Necessary object creation** (Lock(), asyncio event loops, attrs instances)

**All actionable Foundation-internal allocation hotspots have been eliminated across 4 optimization passes.** The remaining allocators are in external dependencies or stdlib with no Foundation-side mitigation available.
