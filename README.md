# KColorConverter
A library for converting colors between multiple formats.

This library provides tools to handle and convert colors between formats such as RGB, RGBA, HEX6, and HEX8.
It offers flexible handling of input formats (strings, tuples) and output specifications. Ideal for developers
working with color manipulations in Python.

## Key Features:
- **Convert between formats**:
  - RGB (e.g., `(255, 0, 0)`)
  - RGBA (e.g., `(255, 0, 0, 1.0)`)
  - HEX6 (e.g., `#FF0000`)
  - HEX8 (e.g., `#FF0000FF`)


- **Customizable output formats**:
  - Use format strings like `III` for integer output or `IIIF` for mixed integer-float output (e.g., `(255, 0, 0, 0.5)`).


- **Helper functions**:
  - Convert integer values (0–255) to floats (0.0–1.0) and vice versa.
  - Automatically determine format types when converting.

## Classes
- **KColorFormat**:
  - An enum representing supported color formats (`RGB`, `RGBA`, `HEX6`, `HEX8`).


- **KColorConverter**:
  - The main class providing conversion methods and utilities.

## Methods
- `KColorConverter.convert(color, output_type, fmt=None)`:
  - Converts a color to the desired output format.
  - `color`: The input color as a string or tuple.
  - `output_type`: The desired format (e.g., `KColorFormat.RGB`).
  - `fmt`: Optional format string for output.


- Helper methods (used internally but can be useful):
  - `int_to_float(value: int)`: Converts an integer (0–255) to a float (0.0–1.0).
  - `float_to_int(value: float)`: Converts a float (0.0–1.0) to an integer (0–255).
  - `_determine_format(values: Tuple)`: Determines the format string based on input types.

## Examples
```python
from kcolorconverter import KColorFormat, KColorConverter

## Convert a HEX color to RGB
rgb = KColorConverter.convert("#FF5733", output_type=KColorFormat.RGB)
print(rgb)  # Output: (255, 87, 51)

## Convert a HEX color to RGBA with a custom format
rgba = KColorConverter.convert("#FF5733", output_type=KColorFormat.RGBA, fmt="IIIF")
print(rgba)  # Output: (255, 87, 51, 1.0)

## Convert an RGB tuple to a HEX6 color
hex6 = KColorConverter.convert((255, 87, 51), output_type=KColorFormat.HEX6)
print(hex6)  # Output: "#FF5733"

## Convert an RGBA tuple to a HEX8 color
hex8 = KColorConverter.convert((255, 87, 51, 128), output_type=KColorFormat.HEX8)
print(hex8)  # Output: "#FF573380"

## Convert an integer to float
print(KColorConverter.int_to_float(128))  # Output: 0.5019607843137255

## Convert a float to integer
print(KColorConverter.float_to_int(0.5))  # Output: 128

For more examples, refer to the GitHub repository: https://github.com/kokaito-git/kcolorconverter```
