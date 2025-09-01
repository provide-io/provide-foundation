# 🚀 Getting Started

## 📦 Installation

Installing `provide.foundation` is straightforward. You can use `pip`, `uv`, or your favorite Python package manager.

### Using pip

To install the latest stable release from PyPI, run:

```bash
pip install provide-foundation
```

### Using uv

If you are using `uv`, the high-performance Python package installer and resolver from Astral, you can install it with:

```bash
uv pip install provide-foundation
```

### Verifying the Installation

To ensure the library was installed correctly, you can run the following command in your terminal:

```bash
python -c "from provide.foundation import logger; logger.info('Installation successful!')"
```

If the installation was successful, you will see a formatted log message:

```
[▶️] Installation successful!
```

### Development Version

If you need the latest development features, you can install the library directly from the `main` branch of our GitHub repository:

```bash
pip install git+https://github.com/provide-io/provide-foundation.git
```

!!! note
    The development version may contain experimental features and is not guaranteed to be stable. For production use, we strongly recommend using a stable release from PyPI.

---

Next, head to the [**Quick Start**](./quick-start.md) guide to write your first log messages.