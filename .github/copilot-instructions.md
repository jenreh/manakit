---
applyTo: "**"
---

# Reflex-Mantine Component Library

**Reflex wrapper library for Mantine UI v8.3.3 components with production-ready examples.**

> **Purpose:** Guide AI coding agents on this codebase's unique patterns and architecture.
> **Tech Stack:** Python 3.12+ · Reflex 0.8.13+ · Mantine UI 8.3.3 · UV workspace

---

## Quick Reference for AI Agents

**Critical architectural patterns unique to this codebase:**

1. **Inheritance-Based Components** - All input components inherit from `MantineInputComponentBase` (~40 common props)
2. **MantineProvider Auto-Injection** - Automatically wraps all apps at priority 44 via `_get_app_wrap_components()`
3. **UV Workspace Structure** - Component library in `components/manakit-mantine/`, demo app in root
4. **Event Handler Transformations** - Components transform raw values to Reflex events via `get_event_triggers()`
5. **Custom CSS Injection** - Components override `_get_custom_code()` for additional stylesheets

---

## Core Architectural Patterns

### 1. Inheritance Hierarchy (WHY: Eliminates code duplication)

```
MantineComponentBase (base for all Mantine components)
    ↓
MantineInputComponentBase (~40 common input props)
    ↓
Specific Components (PasswordInput, NumberInput, DateInput, etc.)
```

**CRITICAL:** When creating new input components, **ONLY define component-specific props**:

```python
# ✅ CORRECT - Only unique props
class NumberInput(MantineInputComponentBase):
    tag = "NumberInput"
    min: Var[int | float] = None
    max: Var[int | float] = None
    decimal_scale: Var[int] = None
    # All common props (label, placeholder, error, etc.) inherited automatically

# ❌ WRONG - Don't redeclare inherited props
class BadInput(MantineInputComponentBase):
    tag = "BadInput"
    label: Var[str] = None          # Already in MantineInputComponentBase!
    placeholder: Var[str] = None    # Already in MantineInputComponentBase!
```

**Common inherited props include:**
- Input.Wrapper: `label`, `description`, `error`, `required`, `with_asterisk`
- Visual: `variant`, `size`, `radius`
- State: `value`, `default_value`, `placeholder`, `disabled`
- HTML: `name`, `id`, `aria_label`, `max_length`, `pattern`
- Sections: `left_section`, `right_section`, `left_section_width`, `right_section_width`
- Mantine styles: `w`, `maw`, `miw`, `m`, `mt`, `mb`, `ml`, `mr`, `mx`, `my`, `p`
- Events: `on_change`, `on_focus`, `on_blur`, `on_key_down`, `on_key_up`, `on_input`

### 2. MantineProvider Auto-Injection (WHY: Ensures all components have required context)

**NEVER manually wrap components in MantineProvider** - it's automatically injected:

```python
# In MantineComponentBase
@staticmethod
def _get_app_wrap_components() -> dict[tuple[int, str], rx.Component]:
    return {
        (44, "MantineProvider"): MemoizedMantineProvider.create(),
    }
```

**Why this matters:**
- MantineProvider respects Reflex's color mode system
- Custom JavaScript integration at `components/manakit-mantine/src/manakit_mantine/mantine_provider.js`
- Injects required CSS and theme context for all Mantine components

### 3. Event Handler Transformations (WHY: Mantine sends raw values, Reflex expects specific formats)

Some Mantine components send raw values instead of events. Transform via `get_event_triggers()`:

```python
# NumberInput sends number directly, not event.target.value
class NumberInput(MantineInputComponentBase):
    on_change: EventHandler[lambda value: [value]] = None

# DateInput sends null when cleared - convert to empty string for Reflex state
def _date_input_on_change(value: Var) -> list[Var]:
    return [rx.Var(f"({value} ?? '')", _var_type=str)]

class DateInput(MantineDateInputBase):
    def get_event_triggers(self) -> dict[str, Any]:
        return {
            **super().get_event_triggers(),
            "on_change": _date_input_on_change,
        }
```

### 4. Custom CSS Injection (WHY: Additional Mantine packages need their own stylesheets)

Override `_get_custom_code()` for components requiring extra CSS:

```python
class NavigationProgress(MantineComponentBase):
    library = "@mantine/nprogress@8.3.3"

    def _get_custom_code(self) -> str:
        return """import '@mantine/core/styles.css';
import '@mantine/nprogress/styles.css';
import { nprogress } from '@mantine/nprogress';

// Expose API globally for Reflex control
if (typeof window !== 'undefined') {
    window.nprogress = nprogress;
}"""
```

### 5. External Dependencies (WHY: NPM packages must be explicitly declared)

Declare via `lib_dependencies` for NPM packages:

```python
class DateInput(MantineDateInputBase):
    library = "@mantine/dates@^8.3.3"
    lib_dependencies: list[str] = ["dayjs@1.11.13"]  # DateInput needs dayjs

class RichTextEditor(NoSSRComponent):
    library = "@mantine/tiptap@8.3.3"
    lib_dependencies: list[str] = [
        "@tiptap/react@2.12.2",
        "@tiptap/starter-kit@2.12.2",
        # ... other tiptap extensions
    ]
```

---

## UV Workspace Structure (WHY: Monorepo with publishable component + demo app)

```
reflex-mantine/
├── components/
│   └── manakit-mantine/           # Publishable component library
│       ├── src/manakit_mantine/   # Component source code
│       │   ├── base.py            # MantineComponentBase, MantineInputComponentBase
│       │   ├── input.py           # Input components
│       │   ├── tiptap.py          # Rich text editor
│       │   └── mantine_provider.js # Custom provider with color mode
│       └── pyproject.toml         # Component package config
├── examples/                       # Demo application
│   ├── pages/                     # Example pages for each component
│   └── main.py                    # App entry point
├── pyproject.toml                 # Workspace root config
└── uv.lock                        # Unified lockfile
```

**Key points:**
- `manakit-mantine` is published to PyPI independently
- Demo app uses workspace dependency: `manakit-mantine = { workspace = true }`
- Run `uv sync` to install both component library and demo app
- Publish component: `cd components/manakit-mantine && uv build && uv publish`

---

## Development Workflow

### Setup

```bash
# Clone and install
git clone https://github.com/jenreh/reflex-mantine.git
cd reflex-mantine
uv sync                    # Installs workspace components

# Run demo app
reflex run                 # Auto-reload enabled
reflex run --loglevel debug
```

### Creating New Components

**Step 1:** Determine base class
- Input-like component? → Extend `MantineInputComponentBase`
- General Mantine component? → Extend `MantineComponentBase`
- External library? → Extend `rx.Component`

**Step 2:** Implement component (ONLY unique props)

```python
from manakit_mantine.base import MantineInputComponentBase
from reflex.vars.base import Var

class MyInput(MantineInputComponentBase):
    tag = "MyInput"
    alias = "MantineMyInput"  # Optional: avoid name collisions
    
    # Only component-specific props
    custom_prop: Var[str] = None
    special_mode: Var[bool] = None

# Export convenience function
my_input = MyInput.create
```

**Step 3:** Add to `manakit_mantine/__init__.py`

```python
from manakit_mantine.my_input import MyInput, my_input

__all__ = ["MyInput", "my_input", ...]
```

**Step 4:** Create example page in `examples/pages/`

```python
import reflex as rx
import manakit_mantine as mn

class MyInputState(rx.State):
    value: str = ""

def my_input_page() -> rx.Component:
    return rx.container(
        mn.my_input(
            label="Example",
            value=MyInputState.value,
            on_change=MyInputState.set_value,
        ),
    )
```

**Step 5:** Register page in `examples/main.py`

```python
from examples.pages.my_input_examples import my_input_page

app.add_page(my_input_page, title="My Input", route="/myinput")
```

### Code Quality

```bash
# Lint and format
uv run ruff check --fix
uv run ruff format

# Type checking (if configured)
uv run mypy .
```

---

## Common Patterns

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
# Controlled - value managed by state
mn.input(value=State.value, on_change=State.set_value)

# Uncontrolled - uses default_value
mn.input(default_value="Initial")

# IMaskInput is ALWAYS uncontrolled
mn.imask_input(mask="+1 (000) 000-0000", on_accept=State.handle_accept)
```

### Using Inherited Props

```python
# All input components support these inherited props
mn.password_input(
    # Input.Wrapper props
    label="Password",
    description="Must be at least 8 characters",
    error=State.password_error,
    required=True,
    with_asterisk=True,
    
    # Section props
    left_section=rx.icon("lock"),
    left_section_pointer_events="none",
    
    # Mantine style props
    w="100%",
    maw="500px",
    m="md",
    
    # State props
    placeholder="Enter password",
    value=State.password,
    on_change=State.set_password,
)
```

---

## Type Annotations

Use Reflex-specific type annotations:

```python
from typing import Any, Literal
from reflex.vars.base import Var
from reflex.event import EventHandler

class MyComponent(MantineInputComponentBase):
    # Var[] for reactive props
    variant: Var[Literal["filled", "outlined"]] = None
    max_value: Var[int | float] = None
    
    # EventHandler with lambda signature showing what the handler receives
    on_change: EventHandler[lambda value: [value]] = None
    on_submit: EventHandler[lambda form_data: [form_data]] = None
```

---

## Documentation Standards

Every component should include:

```python
"""Mantine MyInput component wrapper for Reflex.

Provides advanced input functionality with custom features.
See `my_input()` function for detailed usage and examples.

Documentation: https://mantine.dev/core/my-input/
"""

class MyInput(MantineInputComponentBase):
    """Mantine MyInput component.
    
    Based on: https://mantine.dev/core/my-input/
    
    Inherits ~40 common input props from MantineInputComponentBase.
    See `my_input()` function for detailed documentation and examples.
    
    Component-specific props:
        custom_prop: Description of this unique prop
        special_mode: Description of this unique prop
    """
```

---

## Testing Components

Verify inheritance works correctly:

```python
# Test that all inherited props are accessible
mn.my_input(
    # Inherited from MantineInputComponentBase
    label="Test",
    required=True,
    left_section=rx.icon("search"),
    
    # Component-specific
    custom_prop="works",
)
```

---

## Tech Stack Reference

**Core:**
- Python 3.12+ (modern type annotations with `|` union syntax)
- Reflex 0.8.13+ (component framework)
- Mantine UI 8.3.3 (React component library)
- UV (fast Python package manager and workspace manager)

**Component Integration:**
- Reflex `rx.Component` base class
- Mantine React components wrapped as Reflex components
- Custom JavaScript for color mode integration
- NPM dependencies declared via `lib_dependencies`

**Development:**
- Ruff (linting and formatting)
- Conventional Commits (commit message format)
- Workspace monorepo with publishable package

---

## Key Conventions

1. **Never redeclare inherited props** - Check `MantineInputComponentBase` before adding props
2. **Don't manually wrap in MantineProvider** - Auto-injected via `_get_app_wrap_components()`
3. **Transform event handlers when needed** - Override `get_event_triggers()` for custom value handling
4. **Inject CSS via `_get_custom_code()`** - For components needing additional stylesheets
5. **Use workspace dependencies** - `manakit-mantine = { workspace = true }` in pyproject.toml
6. **Follow Reflex patterns** - Separate state from view, use `rx.State` for reactivity
7. **Document with Mantine links** - Reference official Mantine docs for each component

---

## Quick Troubleshooting

**Component props not working?**
- Check if prop is already inherited from `MantineInputComponentBase`
- Verify component extends correct base class

**MantineProvider errors?**
- Provider is auto-injected - don't manually add it
- Check `_get_app_wrap_components()` is not overridden incorrectly

**Event handler not firing?**
- Check if component needs `get_event_triggers()` override
- Verify event handler signature matches lambda type

**Styles not applying?**
- Ensure `_get_custom_code()` imports required CSS
- Check if component needs `lib_dependencies` for NPM packages

**Workspace dependency issues?**
- Run `uv sync` to sync workspace
- Verify `pyproject.toml` has correct workspace member paths
