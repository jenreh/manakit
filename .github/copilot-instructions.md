---
applyTo: "**"
---

# Reflex-Mantine Component Library Instructions

**AI coding agent instructions for a Reflex wrapper library for Mantine UI components.**

> **Tech Stack:** Python 3.12+ · Reflex 0.8.13+ · Mantine 8.3+ · UV workspace · React 18
> **Purpose:** Guide AI agents to understand unique architectural patterns and workflows

---

## 🎯 Core Architecture Patterns

### Inheritance-Based Component Design
**Critical:** ALL input components inherit from `MantineInputComponentBase` to eliminate code duplication of ~40 common props.

```python
# ✅ Correct - only define component-specific props
class NumberInput(MantineInputComponentBase):
    tag = "NumberInput"
    min: Var[int | float] = None  # Component-specific only
    max: Var[int | float] = None
    # All common props inherited: label, placeholder, value, on_change, etc.

# ❌ Wrong - don't redeclare inherited props  
class BadInput(MantineInputComponentBase):
    label: Var[str] = None  # Already in base class!
```

**Base Class Selection:**
- Input-like components → `MantineInputComponentBase`
- General Mantine components → `MantineComponentBase` 
- External libraries → `rx.Component`

### MantineProvider Auto-Injection
**Critical:** MantineProvider is automatically injected at priority 44 via `_get_app_wrap_components()`. Never manually wrap apps - it happens automatically.

```python
# This happens automatically - don't add manually
@staticmethod
def _get_app_wrap_components() -> dict[tuple[int, str], rx.Component]:
    return {
        (44, "MantineProvider"): MemoizedMantineProvider.create(),
    }
```

### UV Workspace Structure
**Key distinction:** Publishable component library vs demo app:
- `components/manakit-mantine/src/manakit_mantine/` → Component source (gets published)
- `reflex_mantine/` → Demo app with examples
- `pyproject.toml` workspace manages both

---

## 🔧 Component Development Workflow

### Creating New Components
1. **Determine base class** (see architecture patterns above)
2. **Create component with minimal props:**

```python
from manakit_mantine.base import MantineInputComponentBase

class MyInput(MantineInputComponentBase):
    tag = "MyInput"  # React component name
    alias = "MantineMyInput"  # Optional: avoid name collisions
    
    # Only component-specific props
    custom_prop: Var[str] = None
```

3. **Export in `__init__.py`:**
```python
from .my_input import MyInput, my_input
__all__ = ["MyInput", "my_input", ...]
```

4. **Create example page** in `reflex_mantine/pages/my_input_examples.py`
5. **Register page** in `reflex_mantine/reflex_mantine.py`

### Event Handler Transformations
Some Mantine components send raw values instead of events:

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

### Custom CSS Integration
Components requiring additional CSS override `_get_custom_code()`:

```python
class NavigationProgress(MantineComponentBase):
    library = "@mantine/nprogress@8.2.5"
    
    def _get_custom_code(self) -> str:
        return """import '@mantine/core/styles.css';
import '@mantine/nprogress/styles.css';
// Component-specific setup here"""
```

### External Dependencies
Declare NPM packages via `lib_dependencies`:

```python
class DateInput(MantineDateInputBase):
    library = "@mantine/dates@^8.2.5"
    lib_dependencies: list[str] = ["dayjs@1.11.13"]
```

---

## ⚡ Development Commands

```bash
# Setup (uses uv workspace)
uv sync

# Run demo app with hot reload
reflex run

# Lint and format
uv run ruff check --fix
uv run ruff format

# Test components
uv run pytest
```

---

## 📋 Quality Standards

### Type Safety (Python 3.12+)
```python
from typing import Literal
from reflex.vars.base import Var
from reflex.event import EventHandler

class MyComponent(MantineInputComponentBase):
    variant: Var[Literal["filled", "outlined"]] = None
    on_change: EventHandler[lambda value: [value]] = None
```

### Component Documentation
```python
"""Mantine MyInput component wrapper.

Based on: https://mantine.dev/core/my-input/
Inherits common props from MantineInputComponentBase.
"""
class MyInput(MantineInputComponentBase):
    """Mantine MyInput component.
    
    See `my_input()` function for usage examples.
    """
```

### Prop Aliasing
Python snake_case automatically converts to React camelCase:
```python
# These are automatically aliased
default_value → defaultValue
with_asterisk → withAsterisk  
left_section → leftSection
max_length → maxLength
```

---

## 🚨 Common Patterns to Follow

### State Management
```python
class InputState(rx.State):
    value: str = ""
    error: str = ""
    
    def validate(self) -> None:
        if len(self.value) < 3:
            self.error = "Too short"
        else:
            self.error = ""
```

### Controlled vs Uncontrolled
```python
# ✅ Controlled - value managed by state
mn.input(value=State.value, on_change=State.set_value)

# ✅ Uncontrolled - uses default_value
mn.input(default_value="Initial")

# ⚠️ IMaskInput is ALWAYS uncontrolled
mn.masked_input(mask="+1 (000) 000-0000", on_accept=State.handle_accept)
```

### Input Sections (Icons/Buttons)
```python
mn.input(
    placeholder="Search...",
    left_section=rx.icon("search"),
    left_section_pointer_events="none",  # Click-through
    right_section=rx.button("Clear", on_click=State.clear),
    right_section_pointer_events="all",  # Clickable
)
```

---

## 🔍 Key Files Reference

- `components/manakit-mantine/src/manakit_mantine/base.py` - Base classes with all common props
- `components/manakit-mantine/src/manakit_mantine/inputs.py` - Input component examples
- `reflex_mantine/pages/` - Live examples of all patterns
- `pyproject.toml` - UV workspace configuration
- `rxconfig.py` - Reflex app configuration

**Focus development in:**
- `components/manakit-mantine/src/manakit_mantine/` (component source)
- `reflex_mantine/` (demo app with examples)

---

**Remember:** This codebase eliminates code duplication through inheritance. When in doubt, check what props already exist in the base classes before adding new ones.