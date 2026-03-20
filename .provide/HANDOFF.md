# Memray Memory Profiling Infrastructure

## Problem/Request
Add memray memory allocation profiling to provide-foundation, establish baselines, and perform optimization passes to reduce memory allocations.

## Changes Completed

### Infrastructure (new files)
- `scripts/memray_{logging,serialization,config}_stress.py` -- Stress workloads
- `scripts/run_memray_stress.py` -- Orchestrator
- `tests/memray/{conftest,test_*_stress}.py` -- Pytest wrappers with baseline comparison (15% threshold)
- `tests/memray/baselines.json` -- Allocation baselines
- `.provide/MEMRAY_BASELINE.md` -- Full measurement and optimization history

### Configuration changes
- `pyproject.toml` -- memray dep, `memray` marker, addopts exclusion
- `.gitignore` -- `memray-output/`
- `wrknv.toml` -- `memray`, `memray.test`, `memray.baseline` tasks

### Optimization Pass 1: Regex pre-compilation
- `security/masking.py` -- Pre-compile 22 patterns at module load
- `serialization/cache.py` -- SHA256 -> MD5 for cache keys

### Optimization Pass 2: Fast paths + allocation elimination
- `security/masking.py` -- Keyword pre-check skips regex on non-secret strings
- `logger/processors/sanitization.py` -- Lazy dict copy
- `serialization/cache.py` -- `hash()` tuple keys (zero intermediate strings)
- `serialization/{json,yaml,toml,ini,env}.py` -- Eliminated duplicate get_cache_key calls
- `hub/events.py` -- Conditional list rebuild; cleanup threshold 10->100
- `testmode/internal.py` -- Skip gc.get_objects() when circuit breakers not imported; use gc.get_referrers()
- `tests/serialization/test_cache_utilities.py` -- Updated for tuple key format

### Optimization Pass 3: False positive elimination + inspect caching
- `security/masking.py` -- Replaced bare "key" with "api", "access", "key=", "key:"
- `testmode/detection.py` -- Cached `is_in_click_testing()` results
- `testmode/orchestration.py` -- Final cache clear after stream reset

### Optimization Pass 4: Init-path allocations
- `config/base.py` -- Cached field names set per class (frozenset)
- `hub/initialization.py` -- `_HubWrapper` __slots__ class replaces per-call `type()` dynamic class creation

### Final Results (4 passes)
| Stress Test | Original Allocs | Final Allocs | Reduction | Memory Reduction |
|-------------|-----------------|-------------|-----------|-----------------|
| Logging | 3,878,431 | 709,987 | **-81.7%** | **-87.0%** |
| Serialization | 420,222 | 320,202 | **-23.8%** | **-6.4%** |
| Config | 313,629 | 108,386 | **-65.5%** | **-73.5%** |

## Checklist for Next Session
- [ ] All remaining hotspots are external (structlog, CPython stdlib) -- fully optimized
- [ ] Pre-existing test failure: `tests/crypto/test_certificate_chains.py` -- expired certificate
- [ ] Consider adding memray tests to CI pipeline
