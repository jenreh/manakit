# Reflex-Mantine

[![PyPI version](https://badge.fury.io/py/reflex-mantine.svg)](https://badge.fury.io/py/reflex-mantine)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pre-release](https://img.shields.io/badge/status-pre--release-orange.svg)](https://github.com/jenreh/reflex-mantine)

**Production-ready Mantine UI input components for Reflex with type safety and comprehensive examples.**

A Reflex wrapper library focusing on [Mantine UI v8.2.5](https://mantine.dev) input components, designed for building robust forms and data entry interfaces in Python web applications.

---

## ✨ Features

- **🎯 Input-Focused** - Comprehensive coverage of form inputs: text, password, number, date, masked inputs, textarea, and rich text editor
- **🔒 Type-Safe** - Full type annotations with IDE autocomplete support for all props and event handlers
- **📚 Rich Examples** - Production-ready code examples for every component with common patterns and edge cases
- **🏗️ Clean Architecture** - Inheritance-based design eliminating code duplication across 40+ common props
- **🎨 Mantine Integration** - Seamless integration with Mantine's theming, color modes, and design system
- **⚡ Modern Stack** - Built on Reflex 0.8.13+ with React 18 and Mantine 8.2.5

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
git clone https://github.com/jenreh/reflex-mantine.git
cd reflex-mantine

# Install with uv (installs workspace components)
uv sync

# Run the demo app
reflex run
```

> **⚠️ Pre-release Notice:** This library is in active development (v0.1.0). APIs may change before the 1.0 release.

---

## 🚀 Quick Start

All Mantine components require wrapping in `MantineProvider` (automatically injected):

```python
import reflex as rx
import manakit_mantine as mn

class FormState(rx.State):
    email: str = ""
    password: str = ""

def login_form() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Login"),

            # Basic input with validation
            mn.form_input(
                label="Email",
                placeholder="you@example.com",
                value=FormState.email,
                on_change=FormState.set_email,
                required=True,
                type="email",
            ),

            # Password input with visibility toggle
            mn.password_input(
                label="Password",
                value=FormState.password,
                on_change=FormState.set_password,
                required=True,
            ),

            rx.button("Sign In", on_click=FormState.handle_login),
            spacing="4",
        ),
        max_width="400px",
    )

app = rx.App()
app.add_page(login_form)
```

---

## 📋 Available Components

| Component | Description | Documentation |
|-----------|-------------|---------------|
| **`form_input`** | Basic text input with variants (default, filled, unstyled) | [Guide](docs/MANTINE_INPUTS_GUIDE.md) |
| **`password_input`** | Password field with visibility toggle | [Examples](/reflex_mantine/pages/password_input_examples.py) |
| **`number_input`** | Numeric input with formatting, min/max, step controls | [Examples](/reflex_mantine/pages/number_input_examples.py) |
| **`date_input`** | Date picker with range constraints and formatting | [Examples](/reflex_mantine/pages/date_input_examples.py) |
| **`masked_input`** | Input masking for phone numbers, credit cards, custom patterns | [Guide](docs/MANTINE_INPUTS_GUIDE.md) |
| **`textarea`** | Multi-line text input with auto-resize | [Guide](docs/MANTINE_TEXTAREA_GUIDE.md) |
| **`rich_text_editor`** | WYSIWYG editor powered by Tiptap | [Guide](docs/MANTINE_TIPTAP_GUIDE.md) |
| **`navigation_progress`** | Page loading progress indicator | [Examples](/reflex_mantine/pages/nprogress_examples.py) |

### Common Props (Inherited by All Inputs)

All input components inherit ~40 common props from `MantineInputComponentBase`:

```python
# Input.Wrapper props
label="Field Label"
description="Helper text"
error="Validation error"
required=True
with_asterisk=True  # Show red asterisk for required fields

# Visual variants
variant="filled"  # "default" | "filled" | "unstyled"
size="md"  # "xs" | "sm" | "md" | "lg" | "xl"
radius="md"  # "xs" | "sm" | "md" | "lg" | "xl"

# State management
value=State.field_value
default_value="Initial value"
placeholder="Enter text..."
disabled=False

# Sections (icons, buttons)
left_section=rx.icon("search")
right_section=rx.button("Clear")
left_section_pointer_events="none"  # Click-through

# Mantine style props
w="100%"  # width
maw="500px"  # max-width
m="md"  # margin
p="sm"  # padding

# Event handlers
on_change=State.handle_change
on_focus=State.handle_focus
on_blur=State.handle_blur
```

---

## 📖 Usage Examples

### Basic Input with Validation

```python
import reflex as rx
import manakit_mantine as mn

class EmailState(rx.State):
    email: str = ""
    error: str = ""

    def validate_email(self):
        if "@" not in self.email:
            self.error = "Invalid email format"
        else:
            self.error = ""

def email_input():
    return mn.form_input(
        label="Email Address",
        description="We'll never share your email",
        placeholder="you@example.com",
        value=EmailState.email,
        on_change=EmailState.set_email,
        on_blur=EmailState.validate_email,
        error=EmailState.error,
        required=True,
        type="email",
        left_section=rx.icon("mail"),
    )
```

### Number Input with Formatting

```python
class PriceState(rx.State):
    price: float = 0.0

def price_input():
    return mn.number_input(
        label="Product Price",
        value=PriceState.price,
        on_change=PriceState.set_price,
        prefix="$",
        decimal_scale=2,
        fixed_decimal_scale=True,
        thousand_separator=",",
        min=0,
        max=999999.99,
        step=0.01,
    )
```

### Masked Input (Phone Number)

```python
class PhoneState(rx.State):
    phone: str = ""

def phone_input():
    return mn.masked_input(
        label="Phone Number",
        mask="+1 (000) 000-0000",
        value=PhoneState.phone,
        on_accept=PhoneState.set_phone,  # Note: on_accept, not on_change
        placeholder="+1 (555) 123-4567",
    )
```

### Date Input with Constraints

```python
from datetime import date, timedelta

class BookingState(rx.State):
    checkin: str = ""

def date_picker():
    today = date.today()
    max_date = today + timedelta(days=365)

    return mn.date_input(
        label="Check-in Date",
        value=BookingState.checkin,
        on_change=BookingState.set_checkin,
        min_date=today.isoformat(),
        max_date=max_date.isoformat(),
        clear_button_props={"aria_label": "Clear date"},
    )
```

### Rich Text Editor

```python
class EditorState(rx.State):
    content: str = "<p>Start typing...</p>"

def editor():
    return mn.rich_text_editor(
        value=EditorState.content,
        on_change=EditorState.set_content,
        toolbar_config=mn.EditorToolbarConfig(
            controls=[
                mn.ToolbarControlGroup.FORMATTING,
                mn.ToolbarControlGroup.LISTS,
                mn.ToolbarControlGroup.LINKS,
            ]
        ),
    )
```

---

## 📚 Documentation

Comprehensive guides are available in the [`docs/`](docs/) directory:

- **[Mantine Inputs Guide](docs/MANTINE_INPUTS_GUIDE.md)** - Complete reference for all input components
- **[Textarea Guide](docs/MANTINE_TEXTAREA_GUIDE.md)** - Multi-line text input patterns
- **[Tiptap Guide](docs/MANTINE_TIPTAP_GUIDE.md)** - Rich text editor configuration
- **[Number Format Quick Reference](docs/NUMBER_FORMAT_QUICK_REF.md)** - Number formatting patterns

### Live Examples

Run the demo app to explore interactive examples:

```bash
# Clone the repository
git clone https://github.com/jenreh/reflex-mantine.git
cd reflex-mantine

# Install dependencies
uv sync

# Run the demo app
reflex run
```

Visit `http://localhost:3000` and navigate through the example pages:

- `/password` - Password input patterns
- `/date` - Date picker examples
- `/number` - Number input formatting
- `/textarea` - Textarea auto-resize
- `/inputs` - Basic input showcase
- `/nprogress` - Navigation progress
- `/tiptap` - Rich text editor

---

## 🏗️ Architecture

### UV Workspace Structure

This project uses **UV workspace** to manage the component library and demo application:

```
reflex-mantine/
├── components/
│   └── reflex-mantine/    # Distributable component library
│       ├── mantine/             # Component source code
│       └── pyproject.toml       # Component package config
├── reflex_mantine/              # Demo application
│   ├── pages/                   # Example pages
│   └── reflex_mantine.py        # App entry point
├── docs/                        # Documentation guides
├── pyproject.toml               # Workspace root config
└── README.md                    # This file
```

The **`reflex-mantine`** package is published to PyPI and can be used independently. The demo app in `reflex_mantine/` serves as both documentation and testing ground.

### Inheritance-Based Design

All input components inherit from `MantineInputComponentBase`, eliminating code duplication:

```python
# Base class provides ~40 common props automatically
class MantineInputComponentBase(MantineComponentBase):
    # Input.Wrapper props (label, description, error, required)
    # Visual variants (variant, size, radius)
    # State props (value, default_value, placeholder)
    # HTML attributes (name, id, aria_label, pattern)
    # Section props (left_section, right_section)
    # Mantine style props (w, maw, m, p)
    # Event handlers (on_change, on_focus, on_blur)
```

**When creating new components, only define component-specific props:**

```python
class NumberInput(MantineInputComponentBase):
    tag = "NumberInput"

    # Only unique props - all common props inherited
    min: Var[int | float] = None
    max: Var[int | float] = None
    decimal_scale: Var[int] = None
    prefix: Var[str] = None
    suffix: Var[str] = None
```

### Critical Integration Patterns

1. **MantineProvider Auto-Injection** - Wraps all apps automatically at priority 44
2. **Custom CSS Injection** - Components override `_get_custom_code()` for Mantine CSS
3. **Event Handler Transformations** - Components transform raw values to Reflex events
4. **External Dependencies** - NPM packages declared via `lib_dependencies`

See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for detailed development guidelines.

---

## 🔧 Requirements

- **Python**: 3.12 or higher
- **Reflex**: 0.8.13 or higher
- **Node.js**: 18+ (for Mantine/React dependencies)

### Key Dependencies

- `@mantine/core@8.3` - Mantine UI library
- `@mantine/dates@^8.2.5` - Date components
- `@mantine/nprogress@8.2.5` - Progress indicator
- `react-imask@7.6.1` - Input masking
- `@tiptap/*` - Rich text editor

---

## 🤝 Contributing

Contributions are welcome! This project follows a structured development workflow:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-component`)
3. **Follow** the architecture guidelines in `.github/copilot-instructions.md`
4. **Add** examples to `reflex_mantine/pages/`
5. **Test** your changes with `reflex run`
6. **Commit** with clear messages (`git commit -m 'Add amazing component'`)
7. **Push** to your branch (`git push origin feature/amazing-component`)
8. **Open** a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/jenreh/reflex-mantine.git
cd reflex-mantine

# Install with uv (recommended) - automatically installs workspace components
uv sync

# Run demo app with hot reload
reflex run

# Run with debug logging
reflex run --loglevel debug
```

### Publishing the Component

The `reflex-mantine` component can be published independently:

```bash
# Navigate to component directory
cd components/manakit-mantine

# Build the package
uv build

# Publish to PyPI
uv publish
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **GitHub**: [https://github.com/jenreh/reflex-mantine](https://github.com/jenreh/reflex-mantine)
- **PyPI**: [https://pypi.org/project/reflex-mantine/](https://pypi.org/project/reflex-mantine/)
- **Reflex Docs**: [https://reflex.dev](https://reflex.dev)
- **Mantine Docs**: [https://mantine.dev](https://mantine.dev)
- **Issues**: [https://github.com/jenreh/reflex-mantine/issues](https://github.com/jenreh/reflex-mantine/issues)

---

## 🙏 Acknowledgments

- **[Reflex](https://reflex.dev)** - The pure Python web framework
- **[Mantine](https://mantine.dev)** - The React component library
- **Community contributors** who helped shape this project

---

**Built with ❤️ for the Reflex community**
