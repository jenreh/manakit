# manakit

[![PyPI version](https://badge.fury.io/py/manakit-mantine.svg)](https://badge.fury.io/py/manakit-mantine)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pre-release](https://img.shields.io/badge/status-pre--release-orange.svg)](https://github.com/jenreh/manakit)

**Production-ready Mantine UI input components for Reflex with type safety and comprehensive examples.**

A Reflex wrapper library focusing on [Mantine UI v8.3.3](https://mantine.dev) input components, designed for building robust forms and data entry interfaces in Python web applications.

---

## ✨ Features

- **🎯 Input-Focused** - Comprehensive coverage of form inputs: text, password, number, date, masked inputs, textarea, and rich text editor
- **🔒 Type-Safe** - Full type annotations with IDE autocomplete support for all props and event handlers
- **📚 Rich Examples** - Production-ready code examples for every component with common patterns and edge cases
- **🏗️ Clean Architecture** - Inheritance-based design eliminating code duplication across 40+ common props
- **🎨 Mantine Integration** - Seamless integration with Mantine's theming, color modes, and design system
- **⚡ Modern Stack** - Built on Reflex 0.8.13+ with React 18 and Mantine 8.3.3

---

## 📦 Installation

### Using pip

```bash
pip install manakit-mantine
```

### Using uv (recommended)

```bash
uv add manakit-mantine
```

### Development Installation

For local development or to run the demo application:

```bash
# Clone the repository
git clone https://github.com/jenreh/manakit.git
cd manakit

# Install with uv (installs workspace components)
uv sync

# Run the demo app
reflex run
```

> **⚠️ Pre-release Notice:** This library is in active development (v0.1.0). APIs may change before the 1.0 release.

## 🙏 Acknowledgments

- **[Reflex](https://reflex.dev)** - The pure Python web framework
- **[Mantine](https://mantine.dev)** - The React component library
- **Community contributors** who helped shape this project

---

**Built with ❤️ for the Reflex community**
