"""Examples demonstrating Mantine DateInput component usage.

This file shows various ways to use the DateInput component from @mantine/dates:
1. Basic date input
2. Custom date format (valueFormat)
3. Min and max date constraints
4. Clearable date input
5. Date validation with state
6. Form integration with multiple dates
7. Disabled state
8. Custom date parser

All examples follow best practices:
- Use w="100%" for proper width control
- Wrap inputs in containers with max_width for responsive design
- Show proper state management patterns
- Demonstrate event handlers and validation
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta
from typing import Any

import manakit_mantine as mn
import reflex as rx

# Constants for validation
MIN_AGE_YEARS = 18
MAX_AGE_YEARS = 120
MAX_BOOKING_DAYS = 365
MIN_AGE_YEARS = 18
MAX_AGE_YEARS = 120


class BasicDateState(rx.State):
    """State for basic date input example."""

    selected_date: str = ""

    def set_selected_date(self, value: str) -> None:
        """Set the selected date."""
        self.selected_date = value


class FormattedDateState(rx.State):
    """State for custom format date input example."""

    appointment_date: str = ""

    def set_appointment_date(self, value: str) -> None:
        """Set the appointment date."""
        self.appointment_date = value


class ConstrainedDateState(rx.State):
    """State for date input with min/max constraints."""

    booking_date: str = ""

    def set_booking_date(self, value: str) -> None:
        """Set the booking date."""
        self.booking_date = value


class ClearableDateState(rx.State):
    """State for clearable date input example."""

    event_date: str = ""  # Allow empty string when cleared

    def set_event_date(self, value: str) -> None:
        """Set the event date."""
        self.event_date = value


class ValidatedDateState(rx.State):
    """State for date validation example."""

    birth_date: str = ""
    birth_date_error: str = ""

    def set_birth_date(self, value: str) -> None:
        """Set the birth date."""
        self.birth_date = value

    async def validate_birth_date(self) -> AsyncGenerator[Any, Any]:
        """Validate birth date is within acceptable age range."""
        if not self.birth_date:
            self.birth_date_error = "Birth date is required"
            yield
            return

        try:
            # Parse the date
            birth = datetime.fromisoformat(self.birth_date)
            today = datetime.now(tz=UTC)

            # Calculate age
            age = (
                today.year
                - birth.year
                - ((today.month, today.day) < (birth.month, birth.day))
            )

            if age < MIN_AGE_YEARS:
                self.birth_date_error = (
                    f"You must be at least {MIN_AGE_YEARS} years old"
                )
            elif age > MAX_AGE_YEARS:
                self.birth_date_error = "Please enter a valid birth date"
            else:
                self.birth_date_error = ""

        except (ValueError, AttributeError):
            self.birth_date_error = "Invalid date format"

        yield


class DateRangeFormState(rx.State):
    """State for form with multiple date inputs."""

    start_date: str = ""
    end_date: str = ""
    start_date_error: str = ""
    end_date_error: str = ""

    def set_start_date(self, value: str) -> None:
        """Set the start date."""
        self.start_date = value

    def set_end_date(self, value: str) -> None:
        """Set the end date."""
        self.end_date = value

    async def validate_dates(self) -> AsyncGenerator[Any, Any]:
        """Validate that start date is before end date."""
        self.start_date_error = ""
        self.end_date_error = ""

        if not self.start_date:
            self.start_date_error = "Start date is required"
            yield
            return

        if not self.end_date:
            self.end_date_error = "End date is required"
            yield
            return

        try:
            start = datetime.fromisoformat(self.start_date)
            end = datetime.fromisoformat(self.end_date)

            if start > end:
                self.end_date_error = "End date must be after start date"
            elif (end - start).days > MAX_BOOKING_DAYS:
                self.end_date_error = "Date range cannot exceed one year"

        except (ValueError, AttributeError):
            self.start_date_error = "Invalid date format"
            self.end_date_error = "Invalid date format"

        yield

    async def submit_form(self) -> AsyncGenerator[Any, Any]:
        """Handle form submission."""
        # Call validate_dates() as async generator
        async for _ in self.validate_dates():
            pass

        if not self.start_date_error and not self.end_date_error:
            yield rx.toast.success(
                f"Booking confirmed from {self.start_date} to {self.end_date}",
                position="top-right",
            )
        else:
            yield rx.toast.error(
                "Please fix the errors before submitting",
                position="top-right",
            )


def basic_date_example() -> rx.Component:
    """Example 1: Basic date input with state binding.

    Demonstrates:
    - Simple date input with label and placeholder
    - State binding with on_change event
    - Display selected date value
    - Proper width using w="100%"
    """
    return rx.vstack(
        rx.heading("Basic Date Input", size="6"),
        rx.text("Simple date input with state binding", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            mn.date_input(
                label="Select a date",
                placeholder="Pick a date",
                value=BasicDateState.selected_date,
                on_change=BasicDateState.set_selected_date,
                w="100%",
            ),
            rx.cond(
                BasicDateState.selected_date != "",
                rx.text(
                    f"Selected date: {BasicDateState.selected_date}",
                    size="2",
                    color_scheme="blue",
                ),
                rx.text("No date selected", size="2", color_scheme="gray"),
            ),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="600px",
    )


def formatted_date_example() -> rx.Component:
    """Example 2: Date input with custom format.

    Demonstrates:
    - Custom date display format using valueFormat prop
    - Different format patterns (YYYY MMM DD)
    - Description text for user guidance
    """
    return rx.vstack(
        rx.heading("Custom Date Format", size="6"),
        rx.text("Date input with custom display format", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            mn.date_input(
                label="Appointment date",
                description="Date will be displayed as: 2025 Jan 15",
                placeholder="Select appointment date",
                value_format="YYYY MMM DD",
                value=FormattedDateState.appointment_date,
                on_change=FormattedDateState.set_appointment_date,
                w="100%",
            ),
            rx.cond(
                FormattedDateState.appointment_date != "",
                rx.text(
                    f"Selected: {FormattedDateState.appointment_date}",
                    size="2",
                    color_scheme="blue",
                ),
                rx.text("No appointment scheduled", size="2", color_scheme="gray"),
            ),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="600px",
    )


def constrained_date_example() -> rx.Component:
    """Example 3: Date input with min and max constraints.

    Demonstrates:
    - Min and max date constraints
    - Dynamic date calculation (today to 30 days ahead)
    - Automatic validation of date range
    """
    # Calculate dates using Python
    today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
    max_date = (datetime.now(tz=UTC) + timedelta(days=30)).strftime("%Y-%m-%d")

    return rx.vstack(
        rx.heading("Date Range Constraints", size="6"),
        rx.text("Date input limited to next 30 days", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            mn.date_input(
                label="Booking date",
                description="Select a date within the next 30 days",
                placeholder="Choose booking date",
                min_date=today,
                max_date=max_date,
                value=ConstrainedDateState.booking_date,
                on_change=ConstrainedDateState.set_booking_date,
                required=True,
                w="100%",
            ),
            rx.cond(
                ConstrainedDateState.booking_date != "",
                rx.text(
                    f"Booking on: {ConstrainedDateState.booking_date}",
                    size="2",
                    color_scheme="green",
                ),
                rx.text("No booking date selected", size="2", color_scheme="gray"),
            ),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="600px",
    )


def clearable_date_example() -> rx.Component:
    """Example 4: Clearable date input.

    Demonstrates:
    - Clearable prop to allow removing date
    - Default value on component load
    - Clear button interaction
    """
    return rx.vstack(
        rx.heading("Clearable Date Input", size="6"),
        rx.text("Date input with clear button", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            mn.date_input(
                label="Event date",
                description="Click the clear button or select same date to clear",
                placeholder="Select event date",
                clearable=True,
                value=ClearableDateState.event_date,
                on_change=ClearableDateState.set_event_date,
                w="100%",
            ),
            rx.cond(
                ClearableDateState.event_date != "",
                rx.text(
                    f"Event scheduled for: {ClearableDateState.event_date}",
                    size="2",
                    color_scheme="purple",
                ),
                rx.text("No event date set", size="2", color_scheme="gray"),
            ),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="600px",
    )


def validated_date_example() -> rx.Component:
    """Example 5: Date input with validation.

    Demonstrates:
    - Age validation (must be 18+)
    - Error message display
    - on_blur event for validation
    - Dynamic error state
    """
    # Calculate min and max birth dates
    today = datetime.now(tz=UTC)
    max_birth_date = (today - timedelta(days=MIN_AGE_YEARS * 365)).strftime("%Y-%m-%d")
    min_birth_date = (today - timedelta(days=MAX_AGE_YEARS * 365)).strftime("%Y-%m-%d")

    return rx.vstack(
        rx.heading("Date Validation", size="6"),
        rx.text("Birth date with age validation (18+)", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            mn.date_input(
                label="Birth date",
                description=f"You must be at least {MIN_AGE_YEARS} years old",
                placeholder="Enter your birth date",
                value=ValidatedDateState.birth_date,
                on_change=ValidatedDateState.set_birth_date,
                on_blur=ValidatedDateState.validate_birth_date,
                error=ValidatedDateState.birth_date_error,
                max_date=max_birth_date,
                min_date=min_birth_date,
                required=True,
                w="100%",
            ),
            rx.cond(
                (ValidatedDateState.birth_date != "")
                & (ValidatedDateState.birth_date_error == ""),
                rx.text(
                    "✓ Valid birth date",
                    size="2",
                    color_scheme="green",
                ),
            ),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="600px",
    )


def date_range_form_example() -> rx.Component:
    """Example 6: Form with multiple date inputs.

    Demonstrates:
    - Multiple related date inputs in a form
    - Date range validation (start < end)
    - Form submission with validation
    - Error handling for both inputs
    """
    return rx.vstack(
        rx.heading("Date Range Form", size="6"),
        rx.text("Form with start and end date validation", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            mn.date_input(
                label="Start date",
                placeholder="Select start date",
                value=DateRangeFormState.start_date,
                on_change=DateRangeFormState.set_start_date,
                error=DateRangeFormState.start_date_error,
                required=True,
                w="100%",
            ),
            mn.date_input(
                label="End date",
                placeholder="Select end date",
                value=DateRangeFormState.end_date,
                on_change=DateRangeFormState.set_end_date,
                error=DateRangeFormState.end_date_error,
                required=True,
                w="100%",
            ),
            rx.button(
                "Book Dates",
                on_click=DateRangeFormState.submit_form,
                size="3",
                variant="solid",
            ),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="600px",
    )


def disabled_date_example() -> rx.Component:
    """Example 7: Disabled date input.

    Demonstrates:
    - Disabled state
    - Default value in disabled state
    - Read-only presentation
    """
    default_date = "2025-12-31"

    return rx.vstack(
        rx.heading("Disabled Date Input", size="6"),
        rx.text("Date input in disabled state", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            mn.date_input(
                label="Fixed deadline",
                description="This date cannot be changed",
                default_value=default_date,
                disabled=True,
                w="100%",
            ),
            rx.text(
                "This input is disabled and cannot be modified",
                size="2",
                color_scheme="gray",
            ),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="600px",
    )


def sizes_variants_example() -> rx.Component:
    """Example 8: Different sizes and variants.

    Demonstrates:
    - Different input sizes (xs, sm, md, lg, xl)
    - Different variants (default, filled, unstyled)
    - Border radius options
    """
    return rx.vstack(
        rx.heading("Sizes & Variants", size="6"),
        rx.text("Date inputs in different sizes and styles", color_scheme="gray"),
        rx.divider(),
        rx.vstack(
            # Size examples
            rx.text("Sizes:", weight="bold", size="3"),
            mn.date_input(
                label="Extra Small (xs)",
                placeholder="Size xs",
                size="xs",
                w="100%",
            ),
            mn.date_input(
                label="Small (sm)",
                placeholder="Size sm",
                size="sm",
                w="100%",
            ),
            mn.date_input(
                label="Medium (md) - default",
                placeholder="Size md",
                size="md",
                w="100%",
            ),
            mn.date_input(
                label="Large (lg)",
                placeholder="Size lg",
                size="lg",
                w="100%",
            ),
            mn.date_input(
                label="Extra Large (xl)",
                placeholder="Size xl",
                size="xl",
                w="100%",
            ),
            # Variant examples
            rx.text("Variants:", weight="bold", size="3", mt="4"),
            mn.date_input(
                label="Default variant",
                placeholder="Default styling",
                variant="default",
                w="100%",
            ),
            mn.date_input(
                label="Filled variant",
                placeholder="Filled background",
                variant="filled",
                w="100%",
            ),
            mn.date_input(
                label="Unstyled variant",
                placeholder="Minimal styling",
                variant="unstyled",
                w="100%",
            ),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="600px",
    )


def date_input_examples_page() -> rx.Component:
    """Main page showing all DateInput examples."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "Mantine DateInput Examples",
                size="8",
                mb="2",
            ),
            rx.text(
                "Comprehensive examples of DateInput component from @mantine/dates",
                size="4",
                color_scheme="gray",
                mb="6",
            ),
            # All examples
            basic_date_example(),
            formatted_date_example(),
            constrained_date_example(),
            clearable_date_example(),
            validated_date_example(),
            date_range_form_example(),
            disabled_date_example(),
            sizes_variants_example(),
            spacing="8",
            width="100%",
        ),
        size="4",
        py="8",
    )
