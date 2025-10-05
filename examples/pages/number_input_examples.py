"""Examples demonstrating Mantine NumberInput component usage.

This module provides comprehensive examples of using the mn.number_input
component in various scenarios including basic numeric input, currency,
percentages, quantity selectors, and form validation.

Run: reflex run
Navigate to: /number-input-examples
"""

from collections.abc import AsyncGenerator
from typing import Any

import manakit_mantine as mn
import reflex as rx

# ============================================================================
# Example 1: Basic Number Input
# ============================================================================


class BasicNumberState(rx.State):
    """State for basic number input example."""

    age: int = 25

    def set_age(self, value: float | str) -> None:
        """Set the age value."""
        # Convert to int, handling string input from the component
        if isinstance(value, str):
            self.age = int(value) if value else 0
        else:
            self.age = int(value)


def basic_number_example() -> rx.Component:
    """Example 1: Basic number input with min/max constraints.

    Demonstrates:
    - Simple number input with label and placeholder
    - Min/max constraints
    - State binding with on_change
    """
    return rx.vstack(
        rx.heading("Example 1: Basic Number Input", size="5"),
        rx.text("Simple age input with constraints (0-120)", size="2"),
        mn.number_input(
            label="Age",
            placeholder="Enter your age",
            description="Must be between 0 and 120",
            value=BasicNumberState.age,
            on_change=BasicNumberState.set_age,
            min=0,
            max=120,
            clamp_behavior="strict",
            w="100%",
        ),
        rx.text(f"Selected age: {BasicNumberState.age}", size="2", weight="bold"),
        spacing="4",
        align="stretch",
        width="100%",
    )


# ============================================================================
# Example 2: Currency Input
# ============================================================================


class CurrencyState(rx.State):
    """State for currency input example."""

    price: float = 0.0

    def set_price(self, value: float | str) -> None:
        """Set the price value."""
        if isinstance(value, str):
            self.price = float(value) if value else 0.0
        else:
            self.price = float(value)


def currency_input_example() -> rx.Component:
    """Example 2: Currency input with prefix and decimal formatting.

    Demonstrates:
    - Prefix for currency symbol
    - Fixed decimal scale for cents
    - Thousand separator
    - Decimal configuration
    """
    return rx.vstack(
        rx.heading("Example 2: Currency Input", size="5"),
        rx.text("Price input with $ prefix and 2 decimals", size="2"),
        mn.number_input(
            label="Price",
            placeholder="0.00",
            description="Enter product price",
            value=CurrencyState.price,
            on_change=CurrencyState.set_price,
            prefix="$",
            decimal_scale=2,
            fixed_decimal_scale=True,
            thousand_separator=",",
            min=0,
            step=0.01,
            w="100%",
        ),
        rx.text(
            f"Price: ${CurrencyState.price:.2f}",
            size="2",
            weight="bold",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


# ============================================================================
# Example 3: Percentage Input
# ============================================================================


class PercentageState(rx.State):
    """State for percentage input example."""

    discount: float = 10.0

    def set_discount(self, value: float | str) -> None:
        """Set the discount value."""
        if isinstance(value, str):
            self.discount = float(value) if value else 0.0
        else:
            self.discount = float(value)


def percentage_input_example() -> rx.Component:
    """Example 3: Percentage input with suffix and step.

    Demonstrates:
    - Suffix for percentage symbol
    - Step increments (5% at a time)
    - Strict clamping to range
    """
    return rx.vstack(
        rx.heading("Example 3: Percentage Input", size="5"),
        rx.text("Discount percentage with 5% increments", size="2"),
        mn.number_input(
            label="Discount",
            placeholder="0",
            description="Select discount percentage",
            value=PercentageState.discount,
            on_change=PercentageState.set_discount,
            suffix="%",
            min=0,
            max=100,
            step=5,
            clamp_behavior="strict",
            w="100%",
        ),
        rx.text(
            f"Applied discount: {PercentageState.discount}%",
            size="2",
            weight="bold",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


# ============================================================================
# Example 4: Quantity Selector
# ============================================================================


class QuantityState(rx.State):
    """State for quantity selector example."""

    quantity: int = 1

    def set_quantity(self, value: float | str) -> None:
        """Set the quantity value."""
        if isinstance(value, str):
            self.quantity = int(value) if value else 1
        else:
            self.quantity = int(value)


def quantity_selector_example() -> rx.Component:
    """Example 4: Quantity selector with increment/decrement controls.

    Demonstrates:
    - Default value
    - Increment/decrement controls
    - Integer-only input
    - Mouse wheel support
    """
    return rx.vstack(
        rx.heading("Example 4: Quantity Selector", size="5"),
        rx.text("Product quantity with controls", size="2"),
        mn.number_input(
            label="Quantity",
            description="Use controls or type a number",
            value=QuantityState.quantity,
            on_change=QuantityState.set_quantity,
            min=1,
            max=100,
            step=1,
            allow_decimal=False,
            allow_mouse_wheel=True,
            w="100%",
        ),
        rx.text(
            f"Cart quantity: {QuantityState.quantity}",
            size="2",
            weight="bold",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


# ============================================================================
# Example 5: Without Controls
# ============================================================================


class NoControlsState(rx.State):
    """State for number input without controls."""

    weight: float = 70.5

    def set_weight(self, value: float | str) -> None:
        """Set the weight value."""
        if isinstance(value, str):
            self.weight = float(value) if value else 0.0
        else:
            self.weight = float(value)


def no_controls_example() -> rx.Component:
    """Example 5: Number input without increment/decrement controls.

    Demonstrates:
    - Hiding controls with hide_controls
    - Decimal input
    - Unit suffix
    """
    return rx.vstack(
        rx.heading("Example 5: Without Controls", size="5"),
        rx.text("Weight input without increment/decrement buttons", size="2"),
        mn.number_input(
            label="Weight",
            placeholder="70.0",
            description="Enter your weight",
            value=NoControlsState.weight,
            on_change=NoControlsState.set_weight,
            suffix=" kg",
            decimal_scale=1,
            min=0,
            max=500,
            hide_controls=True,
            w="100%",
        ),
        rx.text(
            f"Your weight: {NoControlsState.weight} kg",
            size="2",
            weight="bold",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


# ============================================================================
# Example 6: Form with Validation
# ============================================================================


class NumberFormState(rx.State):
    """State for form with number validation."""

    salary: float = 0.0
    salary_error: str = ""

    def set_salary(self, value: float | str) -> None:
        """Set the salary value."""
        if isinstance(value, str):
            self.salary = float(value) if value else 0.0
        else:
            self.salary = float(value)

    async def validate_salary(self) -> AsyncGenerator[Any, Any]:
        """Validate salary is within reasonable range."""
        if self.salary <= 0:
            self.salary_error = "Salary must be greater than 0"
        elif self.salary < 1000:
            self.salary_error = "Minimum salary is $1,000"
        elif self.salary > 1000000:
            self.salary_error = "Please enter a realistic salary"
        else:
            self.salary_error = ""
        yield

    async def submit_form(self) -> AsyncGenerator[Any, Any]:
        """Handle form submission."""
        async for _ in self.validate_salary():
            pass

        if not self.salary_error:
            yield rx.toast.success(
                f"Annual salary set to ${self.salary:,.2f}",
                position="top-right",
            )
        else:
            yield rx.toast.error(
                "Please fix the errors before submitting",
                position="top-right",
            )


def number_form_example() -> rx.Component:
    """Example 6: Form with number validation.

    Demonstrates:
    - Form integration
    - Custom validation
    - Error display
    - Toast notifications
    """
    return rx.vstack(
        rx.heading("Example 6: Form with Validation", size="5"),
        rx.text("Salary input with validation", size="2"),
        rx.form.root(
            rx.vstack(
                mn.number_input(
                    label="Annual Salary",
                    placeholder="50000",
                    description="Enter your expected annual salary",
                    error=NumberFormState.salary_error,
                    value=NumberFormState.salary,
                    on_change=NumberFormState.set_salary,
                    on_blur=NumberFormState.validate_salary,
                    prefix="$",
                    thousand_separator=",",
                    decimal_scale=2,
                    min=0,
                    required=True,
                    w="100%",
                ),
                rx.button("Submit", type="submit", size="3"),
                spacing="4",
                align="stretch",
            ),
            on_submit=NumberFormState.submit_form,
            width="100%",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


# ============================================================================
# Example 7: Different Thousand Separators
# ============================================================================


class ThousandSeparatorState(rx.State):
    """State for thousand separator examples."""

    amount_comma: float = 1234567.89
    amount_space: float = 1234567.89
    amount_lakh: float = 1234567.89

    def set_amount_comma(self, value: float | str) -> None:
        """Set the comma separator amount."""
        if isinstance(value, str):
            self.amount_comma = float(value) if value else 0.0
        else:
            self.amount_comma = float(value)

    def set_amount_space(self, value: float | str) -> None:
        """Set the space separator amount."""
        if isinstance(value, str):
            self.amount_space = float(value) if value else 0.0
        else:
            self.amount_space = float(value)

    def set_amount_lakh(self, value: float | str) -> None:
        """Set the lakh style amount."""
        if isinstance(value, str):
            self.amount_lakh = float(value) if value else 0.0
        else:
            self.amount_lakh = float(value)


def thousand_separator_example() -> rx.Component:
    """Example 7: Different thousand separator styles.

    Demonstrates:
    - Comma separator (1,000,000)
    - Space separator (1 000 000)
    - Lakh style (1,00,000)
    """
    return rx.vstack(
        rx.heading("Example 7: Thousand Separators", size="5"),
        rx.text("Different grouping styles for large numbers", size="2"),
        mn.number_input(
            label="Comma Separator (Western)",
            description="1,234,567.89",
            value=ThousandSeparatorState.amount_comma,
            on_change=ThousandSeparatorState.set_amount_comma,
            thousand_separator=",",
            thousands_group_style="thousand",
            decimal_scale=2,
            w="100%",
        ),
        mn.number_input(
            label="Space Separator",
            description="1 234 567.89",
            value=ThousandSeparatorState.amount_space,
            on_change=ThousandSeparatorState.set_amount_space,
            thousand_separator=" ",
            thousands_group_style="thousand",
            decimal_scale=2,
            w="100%",
        ),
        mn.number_input(
            label="Lakh Style (Indian)",
            description="12,34,567.89",
            value=ThousandSeparatorState.amount_lakh,
            on_change=ThousandSeparatorState.set_amount_lakh,
            thousand_separator=",",
            thousands_group_style="lakh",
            decimal_scale=2,
            w="100%",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


# ============================================================================
# Example 8: Disabled and Read-Only
# ============================================================================


def disabled_readonly_example() -> rx.Component:
    """Example 8: Disabled and read-only states.

    Demonstrates:
    - Disabled input (cannot interact)
    - Read-only input (can select but not edit)
    """
    return rx.vstack(
        rx.heading("Example 8: Disabled & Read-Only", size="5"),
        rx.text("Different input states", size="2"),
        mn.number_input(
            label="Disabled Input",
            value=42,
            disabled=True,
            description="This input is disabled",
            w="100%",
        ),
        mn.number_input(
            label="Read-Only Input",
            value=99,
            read_only=True,
            description="This input is read-only (can copy but not edit)",
            w="100%",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


# ============================================================================
# Main Examples Page
# ============================================================================


def number_input_examples_page() -> rx.Component:
    """Main page showcasing all NumberInput examples."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("NumberInput Examples", size="9"),
            rx.text(
                "Comprehensive examples of NumberInput component from @mantine/core",
                size="4",
                color="gray",
            ),
            rx.link(
                "← Back to Home",
                href="/",
                size="3",
            ),
            # Grid layout for examples
            rx.grid(
                rx.card(
                    basic_number_example(),
                    padding="4",
                    border="1px solid #e0e0e0",
                    border_radius="8px",
                ),
                rx.card(
                    currency_input_example(),
                    padding="4",
                    border="1px solid #e0e0e0",
                    border_radius="8px",
                ),
                rx.card(
                    percentage_input_example(),
                    padding="4",
                    border="1px solid #e0e0e0",
                    border_radius="8px",
                ),
                rx.card(
                    quantity_selector_example(),
                    padding="4",
                    border="1px solid #e0e0e0",
                    border_radius="8px",
                ),
                rx.card(
                    no_controls_example(),
                    padding="4",
                    border="1px solid #e0e0e0",
                    border_radius="8px",
                ),
                rx.card(
                    number_form_example(),
                    padding="4",
                    border="1px solid #e0e0e0",
                    border_radius="8px",
                ),
                rx.card(
                    thousand_separator_example(),
                    padding="4",
                    border="1px solid #e0e0e0",
                    border_radius="8px",
                ),
                rx.card(
                    disabled_readonly_example(),
                    padding="4",
                    border="1px solid #e0e0e0",
                    border_radius="8px",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            spacing="6",
            width="100%",
            padding_y="4rem",
        ),
        size="4",
    )
