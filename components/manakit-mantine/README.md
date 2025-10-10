# manakit-mantine

[![PyPI version](https://badge.fury.io/py/manakit-mantine.svg)](https://badge.fury.io/py/manakit-mantine)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pre-release](https://img.shields.io/badge/status-pre--release-orange.svg)](https://github.com/jenreh/reflex-mantine)

**reflex.dev components based on MantineUI**

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
git clone https://github.com/jenreh/reflex-mantine.git
cd reflex-mantine

# Install with uv (installs workspace components)
uv sync

# Run the demo app
reflex run
```

> **⚠️ Pre-release Notice:** This library is in development. APIs may change before the 1.0 release.

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
| **`action_icon`** | Lightweight button for icons with size, variant, radius, disabled state | [Examples](/reflex_mantine/pages/action_icon_examples.py) |
| **`autocomplete`** | Autocomplete input with string data array | [Examples](/reflex_mantine/pages/autocomplete_examples.py) |
| **`button`** | Button with variants, sizes, gradient, loading states, sections | [Examples](/reflex_mantine/pages/button_examples.py) |
| **`input`** | Polymorphic base input element with sections, variants, sizes | [Examples](/reflex_mantine/pages/input_examples.py) |
| **`json_input`** | JSON input with formatting, validation, parser, pretty printing | [Examples](/reflex_mantine/pages/json_input_examples.py) |
| **`nav_link`** | Navigation link with label, description, icons, nested links, active/disabled states | [Examples](/reflex_mantine/pages/nav_link_examples.py) |
| **`number_formatter`** | Formats numeric input with parser/formatter, returns parsed value | [Examples](/reflex_mantine/pages/number_formatter_examples.py) |
| **`select`** | Dropdown select with data array, inherits input props | [Examples](/reflex_mantine/pages/select_examples.py) |

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

### Action Icon

```python
def action_icon_example():
    return mn.action_icon(
        rx.icon("heart"),
        variant="filled",
        color="red",
        size="lg",
        on_click=State.like_item,
    )
```

### Autocomplete

```python
class SearchState(rx.State):
    query: str = ""

def autocomplete_example():
    return mn.autocomplete(
        label="Search",
        placeholder="Type to search...",
        data=["Apple", "Banana", "Cherry"],
        value=SearchState.query,
        on_change=SearchState.set_query,
    )
```

### Button

```python
def button_example():
    return mn.button(
        "Click me",
        variant="gradient",
        gradient={"from": "blue", "to": "cyan"},
        size="lg",
        on_click=State.handle_click,
    )
```

### Combobox

```python
def combobox_example():
    return mn.combobox(
        label="Select option",
        data=[
            {"value": "react", "label": "React"},
            {"value": "vue", "label": "Vue"},
        ],
        on_option_submit=State.set_selected,
    )
```

### Input

```python
def input_example():
    return mn.input(
        placeholder="Enter text...",
        left_section=rx.icon("search"),
        right_section=rx.button("Clear"),
    )
```

### JSON Input

```python
class JsonState(rx.State):
    data: str = '{"name": "example"}'

def json_input_example():
    return mn.json_input(
        label="JSON Data",
        value=JsonState.data,
        on_change=JsonState.set_data,
        format_on_blur=True,
    )
```

### Nav Link

```python
def nav_link_example():
    return mn.nav_link(
        label="Dashboard",
        left_section=rx.icon("home"),
        active=True,
        on_click=State.navigate_to_dashboard,
    )
```

### Number Formatter

```python
class PriceState(rx.State):
    amount: float = 1234.56

def number_formatter_example():
    return mn.number_formatter(
        value=PriceState.amount,
        prefix="$",
        thousand_separator=",",
        decimal_scale=2,
    )
```

### Select

```python
class SelectState(rx.State):
    choice: str = ""

def select_example():
    return mn.select(
        label="Choose one",
        data=["Option 1", "Option 2", "Option 3"],
        value=SelectState.choice,
        on_change=SelectState.set_choice,
    )
```

## 📚 Documentation

Comprehensive guides are available in the [`docs/`](docs/) directory:

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

The `manakit-mantine` component can be published independently:

```bash
# Navigate to component directory
cd components/manakit-mantine

# Build the package
uv build

# Publish to PyPI
uv publish
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

## Table component

The `table` wrapper provides a flexible data table that mirrors Mantine's
compound component API. Use the `mn.table` namespace to access the main
component and its parts: `mn.table.thead`, `mn.table.tbody`, `mn.table.tr`,
`mn.table.th`, `mn.table.td`, `mn.table.tfoot`, `mn.table.caption`, and
`mn.table.scroll_container`.

Simple examples

Basic table with head and body:

```python
def simple_table():
    return mn.table(
        children=(
            mn.table.thead(
                mn.table.tr(mn.table.th("ID"), mn.table.th("Name"))
            ),
            mn.table.tbody(
                mn.table.tr(mn.table.td(1), mn.table.td("Alice")),
                mn.table.tr(mn.table.td(2), mn.table.td("Bob")),
            ),
        ),
    )
```

Using `Table.ScrollContainer` for horizontal scrolling:

```python
def scroll_table():
    return mn.table.scroll_container(
        mn.table(
            children=(
                mn.table.thead(mn.table.tr(*[mn.table.th(f"Col {i}") for i in range(1, 12)])),
                mn.table.tbody(
                    *[
                        mn.table.tr(*[mn.table.td(f"r{r}c{c}") for c in range(1, 12)])
                        for r in range(1, 6)
                    ]
                ),
            ),
            # Accepts props like sticky_header, sticky_header_offset, with_table_border
            sticky_header=True,
        )
    )
```

Caption and footer example:

```python
def captioned_table():
    return mn.table(
        children=(
            mn.table.caption("Sample data"),
            mn.table.thead(mn.table.tr(mn.table.th("Key"), mn.table.th("Value"))),
            mn.table.tbody(mn.table.tr(mn.table.td("Name"), mn.table.td("Example"))),
            mn.table.tfoot(mn.table.tr(mn.table.th("Total"), mn.table.td("1"))),
        ),
    )
```

Notes

- The `data` prop is supported for rendering simple head/body arrays directly.
- Use `sticky_header` and `sticky_header_offset` to keep headers visible when
  scrolling.
- You can style parts via `styles` / `sx` props or pass attributes using
  Mantine's `attributes` pattern.

## 🙏 Acknowledgments

Built with ❤️ for the Reflex community
