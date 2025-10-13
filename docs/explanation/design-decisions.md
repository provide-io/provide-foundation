# Explanation: Design Decisions

This document explains the intentional design choices in `provide.foundation`. Understanding these decisions helps you evaluate whether the library aligns with your project's requirements and philosophy.

## 1. Hybrid Dependency Management: Service Locator + DI

`provide.foundation` supports both the **Service Locator** and **Dependency Injection (DI)** patterns. This is a deliberate choice to balance convenience with testability.

-   **Service Locator (`get_hub()`, `logger`):** Used for cross-cutting, framework-level concerns like logging and configuration.
    -   **Why?** It's pragmatic. Forcing DI for a utility like a logger pollutes every single constructor in an application for little practical benefit in testability. Global access for infrastructure is a common and effective pattern.
    -   **Mitigation:** The global state is *managed*. The framework provides robust testing utilities to reset and isolate this state between tests, mitigating the primary drawback of global singletons.

-   **Dependency Injection (`Container`, `@injectable`):** Recommended for your application's business logic (services, repositories, etc.).
    -   **Why?** It makes dependencies explicit, which is crucial for writing modular, loosely coupled, and highly testable application code.

**Guideline:** Use Service Locator for framework infrastructure. Use Dependency Injection for your application's components.

## 2. Opinionated Core Stack: `structlog`, `attrs`, `click`

The framework is tightly integrated with a curated set of libraries.

| Tool | Purpose | Why Chosen |
| :--- | :--- | :--- |
| **`structlog`** | Logging | Provides a powerful, composable processor pipeline that is perfect for structured logging and extensibility. |
| **`attrs`** | Data Classes | Offers excellent performance, immutability (`frozen=True`), and validation capabilities that are ideal for configuration and data models. |
| **`click`** | CLI Framework | A mature, battle-tested library for building user-friendly and composable command-line interfaces. |

-   **The Trade-off:** This opinionated choice means that integrating alternatives (like `loguru`, `pydantic`, or `typer`) requires writing adapter layers.
-   **The Benefit:** It provides a cohesive, "it-just-works" experience. The components are guaranteed to work well together, and the framework can leverage the specific strengths of each library to offer a superior developer experience.

## 3. Threading Model: `threading.RLock` for the Registry

The core `Registry` uses a re-entrant thread lock (`threading.RLock`) for synchronization, not an `asyncio.Lock`.

-   **Why?** This makes the registry **universally compatible**. It works seamlessly in synchronous, multi-threaded, and `asyncio`-based applications without any changes. An `asyncio.Lock` would prevent its use in synchronous or multi-threaded code.
-   **The Limitation:** In extremely high-throughput `asyncio` applications (e.g., >10,000 requests/sec) that perform frequent *runtime component registration or lookups in the request hot-path*, the blocking nature of `threading.RLock` could potentially become a bottleneck.
-   **The Reality:** For 99% of applications, this is a non-issue. Component registration and lookups are typically infrequent operations that happen during application startup or outside the hot path. **Best practice is to resolve dependencies once and reuse them**, which completely avoids this issue.

## 4. Scope: A Foundation, Not a Full-Stack Framework

`provide.foundation` intentionally omits features common in full-stack frameworks.

| Included (Foundational) | Excluded (Application-Specific) |
| :--- | :--- |
| Logging & Telemetry | HTTP Server (e.g., FastAPI, Flask) |
| Configuration | Database ORM (e.g., SQLAlchemy) |
| CLI Framework | Template Engine (e.g., Jinja2) |
| Resilience Patterns | Authentication & Authorization Systems |
| Core Utilities | Message Queue Broker Integration |

-   **Why?** The goal is to provide a stable, universal layer that can sit *underneath* any web framework, task queue, or application type. It solves the problems that are common to *all* of them, without dictating how you should build your business logic. This makes it more flexible and long-lasting than a full-stack framework.
