# provide.io Ecosystem Overview

**Last Updated:** January 05, 2026

Welcome to the provide.io ecosystem! This guide helps you understand how our 11+ projects work together to provide a comprehensive suite of tools for Python and Terraform development.

---

## Quick Start Paths

Choose your journey based on your goals:

### 🚀 Building Terraform Providers in Python

**Path:** pyvider → pyvider-components → terraform-provider-pyvider

1. **[pyvider](https://foundry.provide.io/pyvider/)** - Learn the framework for building Terraform providers
2. **[pyvider-components](https://foundry.provide.io/pyvider-components/)** - Study 100+ example components
3. **[terraform-provider-pyvider](https://foundry.provide.io/terraform-provider-pyvider/)** - See a complete working provider

**Time to first provider:** 2-4 hours

---

### 📦 Packaging Python Applications

**Path:** provide-foundation → flavorpack

1. **[provide-foundation](https://foundry.provide.io/foundation/)** - Core utilities and patterns
2. **[flavorpack](https://foundry.provide.io/flavorpack/)** - PSPF packaging system

**Time to first package:** 1-2 hours

---

### 🧪 Testing Infrastructure Code

**Path:** provide-foundation → provide-testkit

1. **[provide-foundation](https://foundry.provide.io/foundation/)** - Core testing utilities
2. **[provide-testkit](https://foundry.provide.io/provide-testkit/)** - Advanced testing patterns

**Time to first test:** 30 minutes

---

### 📝 Generating Provider Documentation

**Path:** pyvider → plating

1. **[pyvider](https://foundry.provide.io/pyvider/)** - Build your provider
2. **[plating](https://foundry.provide.io/plating/)** - Generate Terraform Registry docs

**Time to documentation:** 1 hour

---

## Project Overview

### Core Framework

#### provide-foundation
**Purpose:** Core Python utilities and patterns for the entire ecosystem

**Features:**
- Async-first architecture patterns
- Logging and observability
- HTTP clients with retry/circuit breaker
- CLI scaffolding
- Testing utilities

**Status:** Beta (v0.0.1026)
**When to use:** Building any Python project in the ecosystem
**Documentation:** [provide-foundation docs](https://foundry.provide.io/foundation/)

---

### Terraform Provider Development

#### pyvider
**Purpose:** Framework for building Terraform providers in Python

**Features:**
- Terraform protocol 6 support
- Resource and data source primitives
- Schema system with validation
- State management
- Provider functions
- Testing utilities

**Status:** Alpha (active development)
**When to use:** Building custom Terraform providers in Python
**Documentation:** [pyvider docs](https://foundry.provide.io/pyvider/)

---

#### pyvider-components
**Purpose:** Library of 100+ example components for learning pyvider

**Features:**
- 60+ example resources
- 30+ example data sources
- 10+ example provider functions
- Real-world implementation patterns
- Testing examples

**Status:** Alpha (example library)
**When to use:** Learning pyvider or referencing component patterns
**Documentation:** [pyvider-components docs](https://foundry.provide.io/pyvider-components/)

---

#### terraform-provider-pyvider
**Purpose:** Pre-release Terraform provider built with pyvider for testing and learning

**Features:**
- File operations resources
- HTTP/API data sources
- Template rendering
- Data transformation functions
- Complete working examples

**Status:** Pre-release
**When to use:** Testing pyvider concepts, learning provider usage
**Documentation:** [terraform-provider-pyvider docs](https://foundry.provide.io/terraform-provider-pyvider/)

---

### Type System & Parsing

#### pyvider-cty
**Purpose:** Python implementation of HashiCorp's go-cty type system

**Features:**
- Complete cty type system
- Type-safe value handling
- Terraform type compatibility
- MessagePack serialization
- Terraform type string parsing

**Status:** Alpha
**When to use:** Working with Terraform types in Python
**Documentation:** [pyvider-cty docs](https://foundry.provide.io/pyvider-cty/)

---

#### pyvider-hcl
**Purpose:** HCL (HashiCorp Configuration Language) parsing with cty integration

**Features:**
- HCL2 parsing
- Automatic cty type conversion
- Schema validation
- Terraform variable factories
- Pretty printing

**Status:** Alpha
**When to use:** Parsing HCL configurations in Python
**Documentation:** [pyvider-hcl docs](https://foundry.provide.io/pyvider-hcl/)

---

#### pyvider-rpcplugin
**Purpose:** RPC plugin framework for Terraform protocol implementation

**Features:**
- Terraform protocol 6 support
- gRPC communication
- Plugin lifecycle management
- Type marshaling
- Error handling

**Status:** Production
**When to use:** Implementing Terraform provider protocol
**Documentation:** [pyvider-rpcplugin docs](https://foundry.provide.io/pyvider-rpcplugin/)

---

### Packaging & Distribution

#### flavorpack
**Purpose:** Cross-platform Python application packaging system

**Features:**
- PSPF (Portable Self-contained Package Format)
- Python application packaging
- Cross-platform helpers (macOS, Linux, Windows)
- CLI tooling
- Build orchestration

**Status:** Alpha
**When to use:** Packaging Python applications for distribution
**Documentation:** [flavorpack docs](https://foundry.provide.io/flavorpack/)

---

### Documentation & Build Tools

#### plating
**Purpose:** Async-first documentation generator for Terraform providers

**Features:**
- Terraform Registry-compliant docs
- Automatic template generation
- Component discovery via foundation.hub
- Parallel processing
- Validation

**Status:** Beta
**When to use:** Generating Terraform provider documentation
**Documentation:** [plating docs](https://foundry.provide.io/plating/)

---

### Testing Tools

#### provide-testkit
**Purpose:** Advanced testing utilities for infrastructure code

**Features:**
- Process testing helpers
- File system fixtures
- Async test support
- Quality checking
- pytest integration

**Status:** Alpha
**When to use:** Testing Python infrastructure code
**Documentation:** [provide-testkit docs](https://foundry.provide.io/provide-testkit/)

---

#### tofusoup
**Purpose:** Testing and conformance toolkit for Terraform/OpenTofu

**Features:**
- Provider testing
- Conformance validation
- Test fixtures
- Integration testing

**Status:** Alpha
**When to use:** Testing Terraform provider implementations
**Documentation:** [tofusoup docs](https://foundry.provide.io/tofusoup/)

---

## Dependency Graph

```
provide-foundation (Core)
├── pyvider (Terraform Provider Framework)
│   ├── pyvider-cty (Type System)
│   ├── pyvider-hcl (HCL Parser)
│   ├── pyvider-rpcplugin (RPC Plugin)
│   ├── pyvider-components (Example Components)
│   │   └── terraform-provider-pyvider (Production Provider)
│   ├── plating (Documentation Generator)
│   └── tofusoup (Testing & Conformance)
├── flavorpack (Packaging System)
└── provide-testkit (Testing Utilities)
```

**Key Dependencies:**

- **All projects** depend on `provide-foundation`
- **pyvider ecosystem** (pyvider, components, provider) depends on:
  - pyvider-cty (type system)
  - pyvider-hcl (HCL parsing)
  - pyvider-rpcplugin (protocol implementation)
- **plating** depends on pyvider framework
- **terraform-provider-pyvider** depends on pyvider-components
- **flavorpack** and **provide-testkit** are independent (only depend on foundation)

---

## Integration Points

### 1. Terraform Provider Development Stack

```
Your Provider Code
    ↓
pyvider Framework
    ↓
pyvider-rpcplugin (Protocol)
    ↓
pyvider-cty (Types) + pyvider-hcl (Parsing)
    ↓
Terraform/OpenTofu
```

**Example:**
```python
from pyvider import Provider, Resource
from pyvider.cty import CtyString, CtyObject

# Your provider code uses pyvider framework
# pyvider uses pyvider-rpcplugin for protocol
# pyvider-cty handles type conversions
# Result: Working Terraform provider
```

---

### 2. Documentation Generation

```
Your Provider (pyvider-based)
    ↓
plating (discovers components)
    ↓
Generates Terraform Registry Docs
```

**Example:**
```bash
plating adorn --component-type resource
plating plate --output-dir docs/
# Result: Terraform Registry-compliant documentation
```

---

### 3. Application Packaging

```
Your Python App
    ↓
flavorpack (PSPF packaging)
    ↓
Cross-platform Package
```

**Example:**
```bash
flavorpack package --format pspf
# Result: Portable self-contained package
```

---

### 4. Testing Infrastructure

```
Your Tests (pytest)
    ↓
provide-testkit (test utilities)
    ↓
tofusoup (provider testing)
    ↓
Test Results
```

---

## Common Workflows

### Workflow 1: Building a Complete Terraform Provider

**Objective:** Create, document, and test a custom Terraform provider

**Steps:**

1. **Setup** (provide-foundation)
   ```bash
   uv add provide-foundation
   ```

2. **Create Provider** (pyvider)
   ```bash
   uv add pyvider pyvider-cty pyvider-hcl pyvider-rpcplugin
   # Follow pyvider getting started guide
   ```

3. **Study Examples** (pyvider-components)
   - Browse component catalog
   - Reference implementation patterns
   - Copy tested examples

4. **Generate Documentation** (plating)
   ```bash
   uv tool install plating
   plating adorn --component-type resource
   plating plate --output-dir docs/
   ```

5. **Test Provider** (provide-testkit, tofusoup)
   ```bash
   uv add provide-testkit
   uv tool install tofusoup
   pytest tests/
   ```

6. **Package Provider** (flavorpack, optional)
   ```bash
   uv tool install flavorpack
   flavorpack package --format pspf
   ```

**Time:** 1-2 days for complete workflow

---

### Workflow 2: Package and Distribute a Python Application

**Objective:** Package a Python CLI tool for cross-platform distribution

**Steps:**

1. **Setup** (provide-foundation)
   ```bash
   uv add provide-foundation
   ```

2. **Develop Application**
   - Use foundation patterns (logging, CLI, async)
   - Follow foundation best practices

3. **Package** (flavorpack)
   ```bash
   uv tool install flavorpack
   flavorpack package --format pspf
   ```

4. **Test Package** (provide-testkit)
   ```bash
   uv add provide-testkit
   pytest tests/
   ```

5. **Distribute**
   - Upload to registry
   - Deploy to environments

**Time:** 4-8 hours

---

### Workflow 3: Parse and Validate HCL Configurations

**Objective:** Read and validate Terraform configurations in Python

**Steps:**

1. **Setup** (pyvider-cty, pyvider-hcl)
   ```bash
   uv add pyvider-cty pyvider-hcl
   ```

2. **Parse HCL**
   ```python
   from pyvider.hcl import parse_hcl_to_cty

   hcl_string = """
     name = "example"
     port = 8080
   """
   cty_value = parse_hcl_to_cty(hcl_string)
   ```

3. **Validate Against Schema**
   ```python
   from pyvider.cty import CtyObject, CtyString, CtyNumber

   schema = CtyObject({
       "name": CtyString(),
       "port": CtyNumber(),
   })
   validated = parse_hcl_to_cty(hcl_string, schema=schema)
   ```

**Time:** 30 minutes

---

## Which Project Do I Need?

### Decision Tree

**Question 1:** What are you building?

- **Terraform Provider** → Go to Question 2
- **Python Application** → Go to Question 3
- **Testing Infrastructure** → Go to Question 4
- **Parsing HCL** → Use **pyvider-hcl** + **pyvider-cty**

---

**Question 2:** (Terraform Provider) What stage are you at?

- **Learning** → **pyvider** + **pyvider-components**
- **Building** → **pyvider** + **pyvider-cty** + **pyvider-hcl** + **pyvider-rpcplugin**
- **Documenting** → **plating**
- **Testing** → **provide-testkit** + **tofusoup**
- **All of the above** → Use all pyvider ecosystem projects

---

**Question 3:** (Python Application) What do you need?

- **Core utilities** (logging, HTTP, CLI) → **provide-foundation**
- **Packaging for distribution** → **flavorpack**
- **Testing utilities** → **provide-testkit**

---

**Question 4:** (Testing) What are you testing?

- **Terraform providers** → **tofusoup** + **provide-testkit**
- **Python infrastructure code** → **provide-testkit**
- **General Python code** → **provide-testkit** (or standard pytest)

---

## Version Compatibility

### Current Versions (January 2026)

| Project | Version | Status | Python | Terraform |
|---------|---------|--------|--------|-----------|
| provide-foundation | v0.0.1026 | Beta | 3.11+ | - |
| pyvider | v0.0.x | Alpha | 3.11+ | 1.0+ |
| pyvider-components | v0.0.x | Alpha | 3.11+ | 1.0+ |
| terraform-provider-pyvider | v0.0.x | Pre-release | 3.11+ | 1.0+ |
| pyvider-cty | v0.0.1026 | Alpha | 3.11+ | - |
| pyvider-hcl | v0.3.0 | Pre-release | 3.11+ | - |
| pyvider-rpcplugin | v1.x.x | Production | 3.11+ | 1.0+ |
| flavorpack | v0.2.0 | Alpha | 3.11+ | - |
| plating | v0.0.1026 | Beta | 3.11+ | - |
| provide-testkit | v0.0.1026 | Alpha | 3.11+ | - |
| tofusoup | v0.0.x | Alpha | 3.11+ | 1.0+ |

### Compatibility Matrix

**Python Version Requirements:**
- **All projects:** Python 3.11 or later
- **Recommended:** Python 3.12 for best performance

**Terraform Version Requirements:**
- **pyvider ecosystem:** Terraform 1.0+ or OpenTofu 1.0+
- **Protocol:** Terraform Protocol 6

**Cross-Project Compatibility:**
- All projects use **compatible versions of provide-foundation**
- pyvider ecosystem projects are **version-locked together**
- Independent projects (flavorpack, testkit) can be used **separately**

---

## Frequently Asked Questions

### General Questions

**Q: Do I need to use all projects?**
A: No. Projects are modular. Use only what you need:
- **Terraform provider development** → pyvider ecosystem
- **Python packaging** → flavorpack
- **Testing** → provide-testkit
- **Core utilities** → provide-foundation (used by all)

**Q: What's the relationship between pyvider-components and terraform-provider-pyvider?**
A: pyvider-components is an **example library** for learning. terraform-provider-pyvider is a **production provider** built using those components. Use components for learning; use provider for actual Terraform usage.

**Q: Are these projects production-focused?**
A: Status varies, but most packages are pre-release:
- **Pre-release:** Most packages (APIs may change)
- **Maturing:** pyvider-rpcplugin and provide-foundation (stable core, evolving surface area)

---

### Technical Questions

**Q: Can I use pyvider with existing Terraform providers?**
A: Yes. pyvider providers are standard Terraform providers. They work with any Terraform/OpenTofu version that supports protocol 6.

**Q: Do I need Go to build Terraform providers with pyvider?**
A: No. pyvider is pure Python. No Go toolchain required.

**Q: Can I package non-Python applications with flavorpack?**
A: Currently, flavorpack focuses on Python applications. Other language support is not available yet.

**Q: What's the difference between provide-foundation and provide-foundry?**
A: provide-foundation is the active core framework. provide-foundry may be a separate/older project. Use **provide-foundation**.

---

### Installation Questions

**Q: Should I use uv?**
A: Yes. The ecosystem standardizes on **uv** for dependency management:
```bash
# Recommended
uv add pyvider
```

**Q: Can I install from source?**
A: Yes, all projects support source installation:
```bash
git clone https://github.com/provide-io/pyvider.git
cd pyvider
uv sync
```

## Getting Help

### Documentation
- **This guide:** Ecosystem overview and integration
- **Project docs:** Detailed documentation for each project (linked above)
- **Tutorials:** Hands-on learning paths in project docs

### Community
- **GitHub Issues:** Report bugs and request features
  - [provide-foundation issues](https://github.com/provide-io/provide-foundation/issues)
  - [pyvider issues](https://github.com/provide-io/pyvider/issues)
  - [Other projects]: Check individual GitHub repositories

### Contributing
- All projects welcome contributions
- See individual CONTRIBUTING.md files
- Follow code of conduct
- Join discussions on GitHub

---

## Summary

The provide.io ecosystem provides a comprehensive suite of tools for:

1. **Building Terraform providers in Python** (pyvider ecosystem)
2. **Packaging Python applications** (flavorpack)
3. **Testing infrastructure code** (provide-testkit, tofusoup)
4. **Generating documentation** (plating)
5. **Core utilities for all projects** (provide-foundation)

**Start with:**
- Building providers? → [pyvider](https://foundry.provide.io/pyvider/)
- Packaging apps? → [flavorpack](https://foundry.provide.io/flavorpack/)
- Testing code? → [provide-testkit](https://foundry.provide.io/provide-testkit/)
- Core utilities? → [provide-foundation](https://foundry.provide.io/foundation/)

---

**Questions?** Check project documentation or open an issue on GitHub.

**Ready to start?** Choose your journey from the [Quick Start Paths](#quick-start-paths) above!
