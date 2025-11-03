"""Examples demonstrating Mantine PasswordInput component usage.

This file shows comprehensive examples of how to use the PasswordInput component
in various scenarios, including basic usage, controlled visibility, custom icons,
sections, error states, and password strength indicators.

Run with: reflex run
"""

import reflex as rx

import appkit_mantine as mn
from appkit_user.authentication.templates import navbar_layout

from app.components.navbar import app_navbar

# ============================================================================
# Constants
# ============================================================================

MIN_PASSWORD_LENGTH = 8
WEAK_PASSWORD_LENGTH = 6
MIN_CRITERIA_FOR_FAIR = 3
MIN_CRITERIA_FOR_GOOD = 4


# ============================================================================
# State Management for Examples
# ============================================================================


class PasswordExamplesState(rx.State):
    """State for PasswordInput examples."""

    # Basic password value
    basic_value: str = ""

    # Controlled visibility example
    controlled_password: str = ""
    show_password: bool = False

    # Synchronized visibility example
    sync_password_1: str = ""
    sync_password_2: str = ""
    sync_visible: bool = False

    # Error state example
    error_password: str = ""
    error_message: str = ""

    # Disabled state
    disabled_value: str = "DisabledPassword123"

    # Strength meter example
    strength_password: str = ""
    strength_label: str = ""
    strength_color: str = "red"
    strength_value: int = 0

    # Form validation example
    form_password: str = ""
    form_confirm: str = ""
    form_error: str = ""
    form_submitted: bool = False

    # Explicit setters (avoid deprecation warnings)
    @rx.event
    def set_basic_value(self, value: str) -> None:
        """Set basic password value."""
        self.basic_value = value

    @rx.event
    def set_show_password(self, visible: bool) -> None:
        """Set password visibility."""
        self.show_password = visible

    @rx.event
    def set_controlled_password(self, value: str) -> None:
        """Set controlled password value."""
        self.controlled_password = value

    @rx.event
    def set_sync_visible(self, visible: bool) -> None:
        """Set synchronized visibility state."""
        self.sync_visible = visible

    @rx.event
    def set_sync_password_1(self, value: str) -> None:
        """Set first synchronized password."""
        self.sync_password_1 = value

    @rx.event
    def set_sync_password_2(self, value: str) -> None:
        """Set second synchronized password."""
        self.sync_password_2 = value

    @rx.event
    def set_error_password(self, value: str) -> None:
        """Set error example password and validate."""
        self.error_password = value
        # Validate on change
        if len(value) > 0 and len(value) < MIN_PASSWORD_LENGTH:
            self.error_message = (
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
            )
        else:
            self.error_message = ""

    @rx.event
    def set_strength_password(self, value: str) -> None:
        """Set password and calculate strength."""
        self.strength_password = value

        # Calculate strength based on criteria
        length = len(value)
        has_upper = any(c.isupper() for c in value)
        has_lower = any(c.islower() for c in value)
        has_digit = any(c.isdigit() for c in value)
        has_special = any(not c.isalnum() for c in value)

        # Count criteria met
        criteria_met = sum([has_upper, has_lower, has_digit, has_special])

        # Calculate strength
        if length == 0:
            self.strength_value = 0
            self.strength_label = ""
            self.strength_color = "red"
        elif length < WEAK_PASSWORD_LENGTH:
            self.strength_value = 20
            self.strength_label = "Too short"
            self.strength_color = "red"
        elif length < MIN_PASSWORD_LENGTH:
            self.strength_value = 40
            self.strength_label = "Weak"
            self.strength_color = "orange"
        elif criteria_met < MIN_CRITERIA_FOR_FAIR:
            self.strength_value = 60
            self.strength_label = "Fair"
            self.strength_color = "yellow"
        elif criteria_met < MIN_CRITERIA_FOR_GOOD:
            self.strength_value = 80
            self.strength_label = "Good"
            self.strength_color = "blue"
        else:
            self.strength_value = 100
            self.strength_label = "Strong"
            self.strength_color = "green"

    @rx.event
    def set_form_password(self, value: str) -> None:
        """Set form password."""
        self.form_password = value
        self._validate_form()

    @rx.event
    def set_form_confirm(self, value: str) -> None:
        """Set form confirmation password."""
        self.form_confirm = value
        self._validate_form()

    def _validate_form(self) -> None:
        """Validate password form."""
        if (
            len(self.form_password) > 0
            and len(self.form_password) < MIN_PASSWORD_LENGTH
        ):
            self.form_error = (
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
            )
        elif len(self.form_confirm) > 0 and self.form_password != self.form_confirm:
            self.form_error = "Passwords do not match"
        else:
            self.form_error = ""

    @rx.event
    def submit_form(self) -> None:
        """Submit password form."""
        self._validate_form()
        if not self.form_error and self.form_password:
            self.form_submitted = True


# ============================================================================
# Example 1: Basic Usage
# ============================================================================


def basic_password_input_example() -> rx.Component:
    """Basic PasswordInput with label and description."""
    return rx.card(
        rx.heading("Basic Password Input", size="4"),
        rx.text(
            "Simple password input with label and description",
            size="2",
            color="gray",
        ),
        mn.password_input(
            label="Your password",
            placeholder="Enter password...",
            description="Password must be at least 8 characters",
            required=True,
            w="100%",
            on_change=PasswordExamplesState.set_basic_value,
        ),
        rx.text(f"Value: {PasswordExamplesState.basic_value}", size="1"),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Example 2: Controlled Visibility
# ============================================================================


def controlled_visibility_example() -> rx.Component:
    """PasswordInput with controlled visibility state."""
    return rx.card(
        rx.heading("Controlled Visibility", size="4"),
        rx.text(
            "Control password visibility with external toggle",
            size="2",
            color="gray",
        ),
        mn.password_input(
            label="Password",
            placeholder="Enter password...",
            w="100%",
            visible=PasswordExamplesState.show_password,
            on_visibility_change=PasswordExamplesState.set_show_password,
            on_change=PasswordExamplesState.set_controlled_password,
        ),
        rx.switch(
            checked=PasswordExamplesState.show_password,
            on_change=PasswordExamplesState.set_show_password,
        ),
        rx.text(
            f"Visible: {PasswordExamplesState.show_password}",
            size="1",
        ),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Example 3: Synchronized Visibility
# ============================================================================


def synchronized_visibility_example() -> rx.Component:
    """Multiple PasswordInputs with synchronized visibility."""
    return rx.card(
        rx.heading("Synchronized Visibility", size="4"),
        rx.text(
            "Toggle shows/hides both password fields",
            size="2",
            color="gray",
        ),
        mn.password_input(
            label="Password",
            placeholder="Enter password...",
            w="100%",
            visible=PasswordExamplesState.sync_visible,
            on_visibility_change=PasswordExamplesState.set_sync_visible,
            on_change=PasswordExamplesState.set_sync_password_1,
        ),
        mn.password_input(
            label="Confirm password",
            placeholder="Confirm password...",
            w="100%",
            visible=PasswordExamplesState.sync_visible,
            on_visibility_change=PasswordExamplesState.set_sync_visible,
            on_change=PasswordExamplesState.set_sync_password_2,
        ),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Example 4: Error State
# ============================================================================


def error_state_example() -> rx.Component:
    """PasswordInput with validation and error display."""
    return rx.card(
        rx.heading("Error State", size="4"),
        rx.text(
            "Password must be at least 8 characters",
            size="2",
            color="gray",
        ),
        mn.password_input(
            label="Password",
            placeholder="Enter password...",
            w="100%",
            error=PasswordExamplesState.error_message,
            required=True,
            on_change=PasswordExamplesState.set_error_password,
        ),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Example 5: Disabled State
# ============================================================================


def disabled_state_example() -> rx.Component:
    """Disabled PasswordInput (hides visibility toggle)."""
    return rx.card(
        rx.heading("Disabled State", size="4"),
        rx.text(
            "Disabled password input (no visibility toggle)",
            size="2",
            color="gray",
        ),
        mn.password_input(
            label="Password",
            w="100%",
            value=PasswordExamplesState.disabled_value,
            disabled=True,
        ),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Example 6: With Left Section
# ============================================================================


def left_section_example() -> rx.Component:
    """PasswordInput with lock icon in left section."""
    return rx.card(
        rx.heading("With Left Section", size="4"),
        rx.text(
            "Password input with lock icon",
            size="2",
            color="gray",
        ),
        mn.password_input(
            label="Password",
            placeholder="Enter password...",
            w="100%",
            left_section=rx.icon("lock", size=16),
            left_section_pointer_events="none",
            on_change=PasswordExamplesState.set_basic_value,
        ),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Example 7: Password Strength Indicator
# ============================================================================


def password_strength_example() -> rx.Component:
    """PasswordInput with password strength meter."""
    return rx.card(
        rx.heading("Password Strength Meter", size="4"),
        rx.text(
            "Visual indicator of password strength",
            size="2",
            color="gray",
        ),
        mn.password_input(
            label="Your password",
            placeholder="Enter password...",
            description="Include uppercase, lowercase, numbers, and symbols",
            w="100%",
            on_change=PasswordExamplesState.set_strength_password,
        ),
        rx.cond(
            PasswordExamplesState.strength_value > 0,
            rx.vstack(
                rx.hstack(
                    rx.text("Strength:", size="1", weight="medium"),
                    rx.text(
                        PasswordExamplesState.strength_label,
                        size="1",
                        color=PasswordExamplesState.strength_color,
                    ),
                    spacing="2",
                ),
                rx.progress(
                    value=PasswordExamplesState.strength_value,
                    color=PasswordExamplesState.strength_color,
                ),
                spacing="2",
                width="100%",
            ),
        ),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Example 8: Form Validation
# ============================================================================


def form_validation_example() -> rx.Component:
    """Complete form with password validation."""
    return rx.card(
        rx.heading("Form Validation", size="4"),
        rx.text(
            "Password confirmation with validation",
            size="2",
            color="gray",
        ),
        rx.form(
            rx.vstack(
                mn.password_input(
                    label="Password",
                    placeholder="Enter password...",
                    description="Must be at least 8 characters",
                    w="100%",
                    required=True,
                    on_change=PasswordExamplesState.set_form_password,
                ),
                mn.password_input(
                    label="Confirm password",
                    placeholder="Confirm password...",
                    w="100%",
                    error=PasswordExamplesState.form_error,
                    required=True,
                    on_change=PasswordExamplesState.set_form_confirm,
                ),
                rx.button(
                    "Submit",
                    type="submit",
                    disabled=rx.cond(
                        PasswordExamplesState.form_error != "",
                        True,
                        False,
                    ),
                ),
                spacing="3",
                width="100%",
            ),
            on_submit=PasswordExamplesState.submit_form,
        ),
        rx.cond(
            PasswordExamplesState.form_submitted,
            rx.callout(
                "Password submitted successfully!",
                icon="check",
                color="green",
            ),
        ),
        spacing="3",
        width="100%",
    )


# ============================================================================
# Main App Page
# ============================================================================


@navbar_layout(
    route="/password",
    title="Input Examples",
    navbar=app_navbar(),
    with_header=False,
)
def password_input_examples_page() -> rx.Component:
    """Main page showing all PasswordInput examples."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("PasswordInput Examples", size="9"),
            rx.text(
                "Comprehensive examples of PasswordInput component from @mantine/core",
                size="4",
                color="gray",
            ),
            rx.link(
                "← Back to Home",
                href="/",
                size="3",
            ),
            rx.grid(
                basic_password_input_example(),
                controlled_visibility_example(),
                synchronized_visibility_example(),
                error_state_example(),
                disabled_state_example(),
                left_section_example(),
                password_strength_example(),
                form_validation_example(),
                columns="2",
                spacing="4",
                width="100%",
            ),
            spacing="6",
            width="100%",
            padding_y="8",
        ),
        size="3",
        width="100%",
    )
