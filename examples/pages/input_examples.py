"""Examples demonstrating Mantine Input components usage in Reflex.

This file provides comprehensive examples of using all Mantine Input components:
- Basic Input with variants, sizes, and states
- Input with left/right sections
- Input.Wrapper for complete form fields
- Custom layouts with Input.Label, Input.Description, Input.Error
- Input.Placeholder for button-based inputs
- Input.ClearButton for clearable inputs

Run this file to see interactive examples in action.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

import manakit_mantine as mn
import reflex as rx

# Constants
MIN_USERNAME_LENGTH = 3


# ============================================================================
# State Management for Examples
# ============================================================================


class MantineInputState(rx.State):
    """State for managing Mantine Input examples."""

    # Form field values
    username: str = ""
    email: str = ""
    search_query: str = ""
    phone: str = ""
    password: str = ""

    # UI state
    show_password: bool = False
    username_error: str = ""
    email_error: str = ""

    # Explicit setters for all state variables
    @rx.event
    def set_username(self, value: str) -> None:
        """Set username value."""
        self.username = value

    @rx.event
    def set_email(self, value: str) -> None:
        """Set email value."""
        self.email = value

    @rx.event
    def set_search_query(self, value: str) -> None:
        """Set search query value."""
        self.search_query = value

    @rx.event
    def set_phone(self, value: str) -> None:
        """Set phone value."""
        self.phone = value

    @rx.event
    def set_password(self, value: str) -> None:
        """Set password value."""
        self.password = value

    # Validation
    @rx.event
    async def validate_username(self) -> AsyncGenerator[Any, Any]:
        """Validate username field."""
        if not self.username:
            self.username_error = "Username is required"
        elif len(self.username) < MIN_USERNAME_LENGTH:
            self.username_error = (
                f"Username must be at least {MIN_USERNAME_LENGTH} characters"
            )
        else:
            self.username_error = ""
            yield rx.toast.success("Username is valid!", position="top-right")

    @rx.event
    async def validate_email(self) -> AsyncGenerator[Any, Any]:
        """Validate email field."""
        if not self.email:
            self.email_error = "Email is required"
        elif "@" not in self.email or "." not in self.email:
            self.email_error = "Please enter a valid email address"
        else:
            self.email_error = ""
            yield rx.toast.success("Email is valid!", position="top-right")

    @rx.event
    def clear_search(self) -> None:
        """Clear search query."""
        self.search_query = ""

    @rx.event
    def toggle_password_visibility(self) -> None:
        """Toggle password visibility."""
        self.show_password = not self.show_password


# ============================================================================
# Example Components
# ============================================================================


def basic_input_variants() -> rx.Component:
    """Example: Basic input with different variants."""
    return rx.vstack(
        rx.heading("Input Variants", size="4"),
        rx.text("Different visual styles for inputs", size="2", color="gray"),
        mn.form_input(
            placeholder="Default variant",
            variant="default",
        ),
        mn.form_input(
            placeholder="Filled variant",
            variant="filled",
        ),
        mn.form_input(
            placeholder="Unstyled variant",
            variant="unstyled",
        ),
        spacing="3",
        width="100%",
    )


def input_sizes() -> rx.Component:
    """Example: Input with different sizes."""
    return rx.vstack(
        rx.heading("Input Sizes", size="4"),
        rx.text("From xs to xl", size="2", color="gray"),
        mn.form_input(placeholder="Extra small (xs)", size="xs"),
        mn.form_input(placeholder="Small (sm)", size="sm"),
        mn.form_input(placeholder="Medium (md)", size="md"),
        mn.form_input(placeholder="Large (lg)", size="lg"),
        mn.form_input(placeholder="Extra large (xl)", size="xl"),
        spacing="3",
        width="100%",
    )


def input_with_sections() -> rx.Component:
    """Example: Input with left and right sections."""
    return rx.vstack(
        rx.heading("Input with Sections", size="4"),
        rx.text("Icons and controls in inputs", size="2", color="gray"),
        mn.form_input(
            placeholder="Search...",
            left_section=rx.icon("search"),
            value=MantineInputState.search_query,
            on_change=MantineInputState.set_search_query,
            variant="filled",
            radius="xl",
        ),
        mn.form_input(
            placeholder="Enter email...",
            left_section=rx.icon("mail"),
            right_section_pointer_events="all",
            right_section=rx.icon_button("check", color="green"),
            variant="filled",
        ),
        mn.form_input(
            placeholder="Clearable input",
            value=MantineInputState.search_query,
            on_change=MantineInputState.set_search_query,
            right_section_pointer_events="all",
            right_section=rx.cond(
                MantineInputState.search_query,
                mn.form_input.clear_button(on_click=MantineInputState.clear_search),
                rx.fragment(),
            ),
        ),
        spacing="3",
        width="100%",
    )


def input_wrapper_example() -> rx.Component:
    """Example: Complete form field using Input.Wrapper."""
    return rx.vstack(
        rx.heading("Input.Wrapper", size="4"),
        rx.text("Complete form fields with labels and descriptions", size="2"),
        mn.form_input.wrapper(
            mn.form_input(
                placeholder="johndoe",
                value=MantineInputState.username,
                on_change=MantineInputState.set_username,
                on_blur=MantineInputState.validate_username,
            ),
            label="Username",
            description="Choose a unique username",
            error=MantineInputState.username_error,
            required=True,
        ),
        mn.form_input.wrapper(
            mn.form_input(
                placeholder="you@example.com",
                value=MantineInputState.email,
                on_change=MantineInputState.set_email,
                on_blur=MantineInputState.validate_email,
            ),
            label="Email",
            description="We'll never share your email",
            error=MantineInputState.email_error,
            required=True,
            with_asterisk=True,
        ),
        spacing="4",
        width="100%",
    )


def custom_layout_example() -> rx.Component:
    """Example: Custom layout with individual label/description/error."""
    return rx.vstack(
        rx.heading("Custom Layout", size="4"),
        rx.text(
            "Build custom layouts with separate components",
            size="2",
            color="gray",
        ),
        rx.vstack(
            mn.form_input.label("Phone Number", required=True),
            mn.form_input.description(
                "Enter your phone number (uses IMask for formatting)"
            ),
            mn.masked_input(
                mask="+1 (000) 000-0000",  # Fixed prefix +1, then digit placeholders
                placeholder="+1 (555) 123-4567",
                # Don't use 'value' prop with IMask - it prevents typing!
                # Use on_accept to capture the formatted value
                on_accept=MantineInputState.set_phone,
                left_section=rx.icon("phone"),
                left_section_pointer_events="none",  # Icon is not interactive
                variant="filled",
            ),
            rx.cond(
                MantineInputState.phone == "",
                mn.form_input.error("Phone number is required"),
                rx.fragment(),
            ),
            spacing="2",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


def input_states_example() -> rx.Component:
    """Example: Different input states (disabled, error, etc.)."""
    return rx.vstack(
        rx.heading("Input States", size="4"),
        rx.text("Disabled, error, and other states", size="2", color="gray"),
        mn.form_input(
            placeholder="Disabled input",
            disabled=True,
            value="Cannot edit this",
        ),
        mn.form_input(
            placeholder="Input with error",
            error=True,
            value="Invalid value",
        ),
        mn.form_input(
            placeholder="Required input",
            required=True,
        ),
        spacing="3",
        width="100%",
    )


def input_radius_example() -> rx.Component:
    """Example: Input with different border radius."""
    return rx.vstack(
        rx.heading("Border Radius", size="4"),
        rx.text("Different border radius styles", size="2", color="gray"),
        mn.form_input(placeholder="Extra small radius (xs)", radius="xs"),
        mn.form_input(placeholder="Small radius (sm)", radius="sm"),
        mn.form_input(placeholder="Medium radius (md)", radius="md"),
        mn.form_input(placeholder="Large radius (lg)", radius="lg"),
        mn.form_input(placeholder="Extra large radius (xl)", radius="xl"),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Main Examples Page
# ============================================================================


def form_inputs_showcase() -> rx.Component:
    """Complete showcase of all Mantine Input examples."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "Mantine Input Components",
                size="8",
                margin_bottom="2",
            ),
            rx.text(
                "Comprehensive examples of Mantine Input components in Reflex",
                size="4",
                color="gray",
                margin_bottom="6",
            ),
            rx.divider(),
            # Examples grid - 2 columns
            rx.grid(
                rx.box(
                    basic_input_variants(),
                    padding="4",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 6)}",
                ),
                rx.box(
                    input_sizes(),
                    padding="4",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 6)}",
                ),
                rx.box(
                    input_with_sections(),
                    padding="4",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 6)}",
                ),
                rx.box(
                    input_radius_example(),
                    padding="4",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 6)}",
                ),
                rx.box(
                    input_wrapper_example(),
                    padding="4",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 6)}",
                    grid_column="span 2",
                ),
                rx.box(
                    custom_layout_example(),
                    padding="4",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 6)}",
                ),
                rx.box(
                    input_states_example(),
                    padding="4",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 6)}",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        max_width="1200px",
        padding="8",
        default_color_scheme="light",
    )
