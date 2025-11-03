# Number Format Components - Quick Reference

## Import
```python
from appkit_ui.components import numeric_format, pattern_format
```

## NumericFormat - Quick Examples

### Currency (US Dollar)
```python
numeric_format(
    value=1234.56,
    prefix="$",
    thousand_separator=",",
    decimal_scale=2,
    fixed_decimal_scale=True
)
# Output: $1,234.56
```

### Currency (Euro)
```python
numeric_format(
    value=1234.56,
    suffix=" €",
    thousand_separator=".",
    decimal_separator=",",
    decimal_scale=2,
    fixed_decimal_scale=True
)
# Output: 1.234,56 €
```

### Percentage
```python
numeric_format(
    value=15.5,
    suffix="%",
    decimal_scale=2,
    allow_negative=False
)
# Output: 15.50%
```

## PatternFormat - Quick Examples

### US Phone Number
```python
pattern_format(
    value="1234567890",
    format="+1 (###) ### ####",
    mask="_"
)
# Output: +1 (123) 456 7890
```

### Credit Card
```python
pattern_format(
    value="4111111111111111",
    format="#### #### #### ####",
    mask="_"
)
# Output: 4111 1111 1111 1111
```

### Date (MM/DD/YYYY)
```python
pattern_format(
    value="01012025",
    format="##/##/####",
    mask="_",
    placeholder="MM/DD/YYYY"
)
# Output: 01/01/2025
```

### SSN
```python
pattern_format(
    value="123456789",
    format="###-##-####",
    mask="_"
)
# Output: 123-45-6789
```

## Event Handling

### State Handler
```python
class MyState(rx.State):
    price: float = 0.0
    phone: str = ""

    def handle_price_change(self, values: dict) -> None:
        """Handle numeric format changes."""
        if isinstance(values, dict) and "floatValue" in values:
            self.price = float(values["floatValue"])

    def handle_phone_change(self, values: dict) -> None:
        """Handle pattern format changes."""
        if isinstance(values, dict) and "value" in values:
            self.phone = str(values["value"])
```

### Using in Components
```python
numeric_format(
    value=MyState.price,
    prefix="$",
    thousand_separator=",",
    decimal_scale=2,
    on_value_change=MyState.handle_price_change
)

pattern_format(
    value=MyState.phone,
    format="+1 (###) ### ####",
    on_value_change=MyState.handle_phone_change
)
```

## Display-Only Mode

```python
# Show formatted value without input
numeric_format(
    value=1234567.89,
    display_type="text",
    prefix="$",
    thousand_separator=",",
    decimal_scale=2,
    fixed_decimal_scale=True
)

pattern_format(
    value="1234567890",
    display_type="text",
    format="+1 (###) ### ####"
)
```

## Common Props

### NumericFormat
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str\|int\|float` | - | Current value |
| `prefix` | `str` | - | Text before number |
| `suffix` | `str` | - | Text after number |
| `thousand_separator` | `str\|bool` | `False` | Thousands separator character |
| `decimal_separator` | `str` | `"."` | Decimal separator character |
| `decimal_scale` | `int` | - | Number of decimals |
| `fixed_decimal_scale` | `bool` | `False` | Always show all decimals |
| `allow_negative` | `bool` | `True` | Allow negative numbers |
| `display_type` | `"input"\|"text"` | `"input"` | Input or text display |

### PatternFormat
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str\|int` | - | Current value |
| `format` | `str` | - | Pattern (use `#` for digits) |
| `mask` | `str\|list[str]` | - | Character for unfilled positions |
| `pattern_char` | `str` | `"#"` | Placeholder character |
| `display_type` | `"input"\|"text"` | `"input"` | Input or text display |

## Event Data Structure

### NumericFormat Events
```python
{
    "formattedValue": "$1,234.56",  # With prefix/suffix/separators
    "value": "1234.56",              # Plain string
    "floatValue": 1234.56            # As number
}
```

### PatternFormat Events
```python
{
    "formattedValue": "+1 (123) 456 7890",  # With pattern
    "value": "1234567890"                    # Digits only
}
```

## Styling

Use Reflex's standard styling approach:

```python
numeric_format(
    value=1234.56,
    prefix="$",
    thousand_separator=",",
    decimal_scale=2,
    placeholder="Enter amount",
    disabled=False,
    class_name="custom-input",
    # No style prop - use Reflex's style system instead
)
```

## Full Documentation
See `NUMBER_FORMAT_README.md` for complete documentation and examples.
