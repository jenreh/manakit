---
applyTo: "**"
---

# Reflex-Mantine Component Library

**A comprehensive Reflex wrapper library for Mantine UI components with production-ready examples.**

## Project Architecture

This is a **UV workspace** containing a distributable component library (`components/manakit-mantine/`) and demo application (`examples/`):

- `components/manakit-mantine/src/manakit_mantine/` – Core component wrappers with inheritance hierarchy
- `components/manakit-mantine/src/manakit_mantine/base.py` – Base classes (`MantineComponentBase`, `MantineInputComponentBase`)
- `examples/` – Demo app with example pages showing component usage patterns
- `examples/pages/` – Interactive examples for each component

### Key Design Principle: Inheritance-Based Architecture

**ALL Mantine input components inherit from `MantineInputComponentBase`**, eliminating code duplication:

```python
# Base class provides ~40 common props automatically
class MantineInputComponentBase(MantineComponentBase):
    # Input.Wrapper props (label, description, error, required, with_asterisk)
    # Visual variants (variant, size, radius)
    # State props (value, default_value, placeholder, disabled)
    # HTML attributes (name, id, aria_label, max_length, pattern, etc.)
    # Section props (left_section, right_section with widths and pointer_events)
    # Mantine style props (w, maw, m, mt, mb, ml, mr, mx, my, p, etc.)
    # Event handlers (on_change, on_focus, on_blur, on_key_down, on_key_up)
```

**When creating new components, only define component-specific props:**

```python
# ✅ Correct - only unique props
class NumberInput(MantineInputComponentBase):
    tag = "NumberInput"
    min: Var[int | float] = None
    max: Var[int | float] = None
    decimal_scale: Var[int] = None
    # All common props inherited automatically

# ❌ Wrong - don't redeclare inherited props
class BadInput(MantineInputComponentBase):
    tag = "BadInput"
    label: Var[str] = None  # Already in base class!
    placeholder: Var[str] = None  # Already in base class!
```

## Critical Integration Patterns

### 1. MantineProvider Auto-Injection

**ALL Mantine components require `MantineProvider` wrapper** - auto-injected via `_get_app_wrap_components()` at priority 44. The provider respects Reflex's color mode and injects required CSS through `mantine_provider.js`.

### 2. Custom CSS Injection Pattern

Components requiring additional CSS override `_get_custom_code()`:

```python
class NavigationProgress(MantineComponentBase):
    library = "@mantine/nprogress@8.2.5"

    def _get_custom_code(self) -> str:
        return """import '@mantine/core/styles.css';
import '@mantine/nprogress/styles.css';
if (typeof window !== 'undefined') {
    window.nprogress = nprogress;
}"""
```

### 3. Event Handler Transformations

Some Mantine components send raw values instead of events - transform via `get_event_triggers()`:

```python
# NumberInput sends number directly, not event.target.value
class NumberInput(MantineInputComponentBase):
    on_change: EventHandler[lambda value: [value]] = None

# DateInput sends null when cleared - convert to empty string
def _date_input_on_change(value: Var) -> list[Var]:
    return [rx.Var(f"({value} ?? '')", _var_type=str)]

class DateInput(MantineDateInputBase):
    def get_event_triggers(self) -> dict[str, Any]:
        return {
            **super().get_event_triggers(),
            "on_change": _date_input_on_change,
        }
```

### 4. External Library Dependencies

Declare via `lib_dependencies` for NPM packages:

```python
class IMaskInput(rx.Component):
    library = "react-imask@7.6.1"
    lib_dependencies: list[str] = ["react-imask@7.6.1"]

class DateInput(MantineDateInputBase):
    library = "@mantine/dates@^8.2.5"
    lib_dependencies: list[str] = ["dayjs@1.11.13"]
```

## Development Workflow

### Running the Demo App

```bash
# Install dependencies with UV
uv sync

# Start Reflex dev server (auto-reload enabled)
reflex run

# Or with debug logging
reflex run --loglevel debug
```

Access demo pages at: `/inputs`, `/password`, `/date`, `/number`, `/textarea`, `/nprogress`, `/tiptap`

### Creating New Components

1. **Determine base class:**
   - Input-like? Extend `MantineInputComponentBase`
   - General Mantine? Extend `MantineComponentBase` 
   - External library? Extend `rx.Component`

2. **Implement minimal component:**

```python
from manakit_mantine.base import MantineInputComponentBase

class MyInput(MantineInputComponentBase):
    tag = "MyInput"  # React component name
    alias = "MantineMyInput"  # Optional: avoid name collisions

    # Only component-specific props
    custom_prop: Var[str] = None
    special_mode: Var[bool] = None

# Export convenience function
my_input = MyInput.create
```

3. **Add to `components/manakit-mantine/src/manakit_mantine/__init__.py`:**

```python
from manakit_mantine.my_input import MyInput, my_input

__all__ = ["MyInput", "my_input", ...]
```

4. **Create example page in `examples/pages/`:**

```python
import manakit_mantine as mn
import reflex as rx

class MyInputState(rx.State):
    value: str = ""

    @rx.event
    def set_value(self, val: str) -> None:
        self.value = val

def my_input_page() -> rx.Component:
    return rx.container(
        rx.heading("MyInput Examples"),
        mn.my_input(
            label="Example",
            value=MyInputState.value,
            on_change=MyInputState.set_value,
        ),
    )
```

5. **Register page in `examples/examples.py`:**

```python
from examples.pages.my_input_examples import my_input_page

app.add_page(my_input_page, title="My Input", route="/myinput")
```

## Common Patterns from Examples

### State Management with Validation

```python
class InputState(rx.State):
    username: str = ""
    username_error: str = ""

    @rx.event
    async def validate_username(self) -> AsyncGenerator[Any, Any]:
        if len(self.username) < 3:
            self.username_error = "Must be at least 3 characters"
        else:
            self.username_error = ""
            yield rx.toast.success("Valid!", position="top-right")
```

### Controlled vs Uncontrolled Components

```python
# ✅ Controlled - value managed by state
mn.form_input(value=State.value, on_change=State.set_value)

# ✅ Uncontrolled - uses default_value
mn.form_input(default_value="Initial")

# ⚠️ IMaskInput is ALWAYS uncontrolled - use on_accept, not value
mn.masked_input(mask="+1 (000) 000-0000", on_accept=State.handle_accept)
```

### Input.Wrapper for Complete Form Fields

```python
# All input components support wrapper props inherited from base
mn.password_input(
    label="Password",
    description="Must be at least 8 characters",
    error=State.password_error,
    required=True,
    with_asterisk=True,  # Show red asterisk
    placeholder="Enter password",
)
```

### Left/Right Sections (Icons, Buttons)

```python
# Inherited from MantineInputComponentBase
mn.form_input(
    placeholder="Search...",
    left_section=rx.icon("search"),
    left_section_pointer_events="none",  # Click-through
    right_section=rx.button("Clear", on_click=State.clear),
    right_section_pointer_events="all",  # Clickable
)
```

## Testing Components

Verify inheritance didn't break existing props:

```python
# All inherited props should work
mn.my_input(
    label="Test",  # From MantineInputComponentBase
    required=True,  # From MantineInputComponentBase
    left_section=rx.icon("search"),  # From MantineInputComponentBase
    custom_prop="works",  # Your specific prop
)
```

## Project-Specific Notes

### Package Structure

- **Distributable library:** `components/manakit-mantine/` (published to PyPI as `manakit-mantine`)
- **Demo application:** `examples/` (local development and documentation)
- Use `uv sync` to install workspace dependencies
- Component exports in `src/manakit_mantine/__init__.py`
- Main app entry point: `examples/examples.py`

### Version Management

- Mantine core: `@mantine/core@8.3.3`
- Mantine dates: `@mantine/dates@^8.2.5`  
- Mantine nprogress: `@mantine/nprogress@8.2.5`
- Pin versions to avoid breaking changes

### JavaScript Integration

- `mantine_provider.js` - Color mode integration
- `navigation_progress.js` - Progress bar controls
- `tiptap_wrapper.js` - Rich text editor wrapper
- Reference via component `library` prop with file paths

### Code Quality Standards

**Type Annotations (Python 3.12+):**
```python
from typing import Any, Literal
from reflex.vars.base import Var
from reflex.event import EventHandler

class MyComponent(MantineInputComponentBase):
    variant: Var[Literal["filled", "outlined"]] = None
    max_value: Var[int | float] = None
    on_change: EventHandler[lambda value: [value]] = None
```

**Documentation Standards:**
Every component should have module docstring with Mantine docs link, class docstring, prop comments, and example usage in dedicated page.