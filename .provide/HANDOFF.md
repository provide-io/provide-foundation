# Memory Optimization: Phase 2

## Problem/Request
Phase 1 added custom level guards to `GlobalLoggerProxy`, wrapped ~403 f-string debug() calls, and built the `wrknv.memray` module. Phase 2 addresses three remaining gaps:
1. structlog's `FilteringBoundLogger` eliminates the need for custom proxy guards
2. ~47ms startup overhead from eagerly-loaded optional deps
3. 7 repos with wrknv.toml had no memray integration

## Changes Completed

### Change 1: FilteringBoundLogger as wrapper_class (provide-foundation)

**Core idea:** `structlog.make_filtering_bound_logger(level)` creates a class where methods below `level` are literal `return None` — zero overhead, no processor entry.

**Files modified:**

| File | Change |
|------|--------|
| `logger/setup/processors.py` | `_make_filtering_bound_logger_with_trace(level)` — creates FilteringBoundLogger with `.trace()`, `.is_debug_enabled()`, `.is_trace_enabled()`, permissive nop for kwargs-only calls; clamps TRACE(5) to DEBUG(10) for structlog (TRACE routed via msg()) |
| `logger/setup/processors.py` | `configure_structlog_output()` — computes effective_level as min(default, all module_levels) so module overrides reach `_LevelFilter` |
| `logger/setup/coordinator.py` | Kept `BoundLogger` for internal setup logger (uses `.trace()` directly) |
| `logger/core.py` | Simplified proxy debug/trace to direct forwarding; added standalone `is_debug_enabled()` / `is_trace_enabled()` |
| `logger/__init__.py` | Exports standalone helpers |
| `logger/processors/main.py` | Level filter always late; OTLP respects FilteringBoundLogger level |
| `hub/decorators.py` | Fixed pre-existing `is_trace_enabled()` crash on raw structlog loggers |
| `tests/logger/test_logger_level_guard.py` | 24 tests updated for new forwarding behavior |
| `tests/platform/test_cpu.py` | Fixed patch target for lazy `_cpuinfo_module` |

**Key architectural decisions:**
- `_LevelFilter` still needed: handles per-module level overrides and trace-via-msg() filtering
- FilteringBoundLogger level = min(default_level, all module_levels) — ensures module overrides work
- Permissive nop: Foundation callers sometimes do `log.debug(key=val)` without event string
- TRACE clamped to DEBUG for structlog since TRACE is Foundation-custom (routed through msg())

### Change 1 downstream: pyvider-rpcplugin

| File | Change |
|------|--------|
| `handshake/core.py` | Removed `_is_debug_enabled()` workaround, removed `structlog` import; linter stripped now-unnecessary guards since FilteringBoundLogger handles filtering |

### Change 3: Lazy-load optional dependencies (provide-foundation)

| File | Dep | Saving |
|------|-----|--------|
| `platform/cpu.py` | `cpuinfo` → `_ensure_cpuinfo()` | ~19ms |
| `process/title.py` | `setproctitle` → `_ensure_setproctitle()` | ~10ms |
| `tracer/__init__.py` | OpenTelemetry → `_ensure_otel_available()` + `__getattr__` | ~18ms |

### Change 2: Memray integration across 6 repos

**Tier A — Had scripts, added test harness:**

| Repo | Tests | Scripts |
|------|-------|---------|
| flavorpack | 5 (builder, reader, operations, xor, slot_descriptor) | 5 existing |
| pyvider-cty | 5 (codec, validation, inference, conversion, unify) | 5 existing |

**Tier B — Full scaffold + project-specific scripts:**

| Repo | Tests | Scripts (new) | Hot paths targeted |
|------|-------|---------------|-------------------|
| tofusoup | 3 | 3 (state, wire, discovery) | Terraform state parsing, wire serialization, test discovery |
| bfiles | 2 | 2 (bundler, parser) | File bundling, bundle parsing |
| plating | 3 | 3 (schema, template, docgen) | Schema formatting, template engine, doc generation |
| wrknv | 2 | 2 (task_registry, config_parsing) | Task execution, config parsing |

All repos received: `tests/memray/` scaffold (conftest.py, baselines.json, __init__.py, test wrappers), `wrknv.toml` tasks, `pyproject.toml` markers, `.gitignore` entries.

## Reasoning

- FilteringBoundLogger is the Pythonic solution — structlog handles level filtering at the binding layer before any processor runs
- Lazy imports defer ~47ms of optional dependency loading to first actual use
- Memray test harnesses use the established `wrknv.memray` pattern (runner, fixtures, baselines)

## Summary

3 changes across 8 repos: FilteringBoundLogger replaces custom proxy guards in provide-foundation (5082+ tests pass), lazy imports save ~47ms startup, memray test harnesses added to 6 repos with 20 test wrappers and 10 new stress scripts.

## Checklist for Next Session

- [ ] Establish memray baselines: `MEMRAY_UPDATE_BASELINE=1 pytest tests/memray/ -m memray -v --no-cov` in each repo
- [ ] Verify memray tests pass after baselines: `pytest tests/memray/ -m memray -v --no-cov` in each repo
- [ ] Measure actual startup improvement: `python -X importtime -c "from provide.foundation import logger" 2>&1 | sort -t: -k2 -rn | head -10`
- [ ] Commit changes in provide-foundation
- [ ] Commit changes in pyvider-rpcplugin
- [ ] Commit memray scaffolds in flavorpack, pyvider-cty, tofusoup, bfiles, plating, wrknv
- [ ] Address pre-existing test failures: expired certs in tests/crypto (not_valid_after 2026-02-05), transport client mock issues, file watcher timing issues
- [ ] Consider: skip low-priority repos (provide-testkit, provide-workspace, messometer, provide-foundry) per plan
