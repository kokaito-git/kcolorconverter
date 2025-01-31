"""
KColorConverter is a Python package for converting between different color formats such as RGB, RGBA, and hexadecimal
(HEX6, HEX8).

The package supports the following functionalities:
- Convert color from HEX to RGB or RGBA formats and vice versa.
- Handle color format conversion with flexible handling for both integer and float representations.
- Provide utilities for converting between RGB and RGBA tuples, as well as HEX formats with or without alpha
  transparency.

This package is ideal for developers working with color manipulation in graphical applications, web development, or data
visualization.

Key Strength:
- You don't need to instantiate any specific class objects to convert colors. The `KColorConverter.convert` method can
  be used directly for color conversion.

Examples of usage:

1. **HEX to RGB**:
   >>> from kcolorconverter import KColorConverter
   >>> rgb = KColorConverter.convert("#FF5733", output_type=KColorFormat.RGB)
   >>> print(rgb)
   # (255, 87, 51)

2. **RGB to HEX**:
   >>> rgb = (255, 87, 51)
   >>> hex_color = KColorConverter.convert(rgb, output_type=KColorFormat.HEX6)
   >>> print(hex_color)
   # "#FF5733"

3. **HEX to RGBA**:
   >>> rgba = KColorConverter.convert("#FF5733", output_type=KColorFormat.RGBA)
   >>> print(rgba)
   # (255, 87, 51, 255)

4. **RGBA to RGB**:
   >>> rgba = (255, 87, 51, 255)
   >>> rgb = KColorConverter.convert(rgba, output_type=KColorFormat.RGB)
   >>> print(rgb)
   # (255, 87, 51)

Version: 0.0.2
"""

from .conversion import KColorConverter
from .constants import N, RGB_TUPLE, RGBA_TUPLE, KColorFormat

if __name__ == "__main__":
    rgb_int_a_float = KColorConverter.convert(color="#000000", output_type=KColorFormat.RGBA, fmt="IF")
    print(rgb_int_a_float)
