from typing import Union, Tuple, Optional
from enum import Enum


class KColorFormat(Enum):
    """
    Enum representing supported color formats.

    Attributes:
        RGB: RGB format as a tuple (R, G, B).
        RGBA: RGBA format as a tuple (R, G, B, A).
        HEX6: Hexadecimal format without alpha (e.g., "#RRGGBB").
        HEX8: Hexadecimal format with alpha (e.g., "#RRGGBBAA").
    """
    RGB = "rgb"
    RGBA = "rgba"
    HEX6 = "hex6"
    HEX8 = "hex8"


class KColorConverter:
    """
    Utility class for color format conversions. Supports conversion between RGB, RGBA,
    HEX6, and HEX8 formats. Provides helper methods to handle different types of
    input (strings or tuples) and output formats.

    Formats supported:
    - RGB: Tuple with 3 values (R, G, B).
    - RGBA: Tuple with 4 values (R, G, B, A).
    - HEX6: Hexadecimal color string without alpha (e.g., "#RRGGBB").
    - HEX8: Hexadecimal color string with alpha (e.g., "#RRGGBBAA").

    Args:
        color (str | Tuple[int | float, ...]): The color to convert.
        output_type (KColorFormat): The desired output format.
        fmt (Optional[str]): Format for output, e.g., 'III' or 'IIIF'.

    Returns:
        str | Tuple[int | float, ...]: The converted color.

    Example:
        >>> KColorConverter.convert("#FF5733", output_type=KColorFormat.RGB)
        (255, 87, 51)
        >>> KColorConverter.convert((255, 87, 51), output_type=KColorFormat.HEX6)
        "#FF5733"
    """

    Num = Union[int, float]

    @classmethod
    def convert(
        cls,
        color: Union[str, Tuple[Num, Num, Num, Num], Tuple[Num, Num, Num]],
        output_type: KColorFormat = KColorFormat.RGB,
        fmt: Optional[str] = None,
    ) -> Union[Tuple[Num, Num, Num, Num], Tuple[Num, Num, Num], str]:
        """
        Converts a color from one format to another.

        Args:
            color (str | Tuple[int | float, ...]): Input color in any supported format.
            output_type (KColorFormat): The desired output format (RGB, RGBA, HEX6, HEX8).
            fmt (Optional[str]): Output format string (e.g., 'III', 'IIIF').

        Returns:
            Union[Tuple[int | float, ...], str]: The converted color.

        Raises:
            ValueError: If the input or output format is invalid.

        Examples:
            >>> KColorConverter.convert("#FF5733", output_type=KColorFormat.RGB)
            (255, 87, 51)
            >>> KColorConverter.convert("#FF5733", output_type=KColorFormat.RGBA, fmt="IIIF")
            (255, 87, 51, 1.0)
            >>> KColorConverter.convert((255, 87, 51), output_type=KColorFormat.HEX6)
            "#FF5733"
        """
        if output_type == KColorFormat.RGB:
            return cls._to_rgb(color, fmt)
        elif output_type == KColorFormat.RGBA:
            return cls._to_rgba(color, fmt)
        elif output_type == KColorFormat.HEX6:
            return cls._to_hex6(color)
        elif output_type == KColorFormat.HEX8:
            return cls._to_hex8(color)
        else:
            raise ValueError("Tipo de salida no soportado")

    @staticmethod
    def int_to_float(value: int) -> float:
        """
        Converts an integer (0-255) to a float (0.0-1.0).

        Args:
            value (int): Input value between 0 and 255.

        Returns:
            float: Converted value between 0.0 and 1.0.

        Raises:
            ValueError: If the input value is out of range.

        Examples:
            >>> KColorConverter.int_to_float(255)
            1.0
            >>> KColorConverter.int_to_float(128)
            0.5019607843137255
        """
        if not (0 <= value <= 255):
            raise ValueError("El valor debe estar entre 0 y 255.")
        return value / 255.0

    @staticmethod
    def float_to_int(value: float) -> int:
        """
        Converts a float (0.0-1.0) to an integer (0-255).

        Args:
            value (float): Input value between 0.0 and 1.0.

        Returns:
            int: Converted value between 0 and 255.

        Raises:
            ValueError: If the input value is out of range.

        Examples:
            >>> KColorConverter.float_to_int(1.0)
            255
            >>> KColorConverter.float_to_int(0.5)
            128
        """
        if not (0.0 <= value <= 1.0):
            raise ValueError("El valor debe estar entre 0.0 y 1.0.")
        return round(value * 255)

    @staticmethod
    def _determine_format(values: Tuple[Num, ...]) -> str:
        format_chars = ""
        for value in values:
            if isinstance(value, int):
                format_chars += "I"
            elif isinstance(value, float):
                format_chars += "F"
            else:
                raise ValueError("Unsupported value type")
        return format_chars

    @staticmethod
    def _hex_to_rgb(
        hex_color: str, fmt: Optional[str] = None
    ) -> Tuple[Num, Num, Num]:
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        if len(hex_color) not in {3, 6}:
            raise ValueError("El color hexadecimal debe tener 3 o 6 caracteres.")

        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        if fmt is None:
            fmt = KColorConverter._determine_format((r, g, b))

        return KColorConverter._format_rgb((r, g, b), fmt)

    @staticmethod
    def _hex_to_rgba(
        hex_color: str, fmt: Optional[str] = None
    ) -> Tuple[Num, Num, Num, Num]:
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        if len(hex_color) not in {3, 4, 6, 8}:
            raise ValueError(
                "El color hexadecimal debe tener {3, 4, 6, 8} caracteres."
            )

        # Full alpha if not specified
        if len(hex_color) == 3:
            hex_color += "F"
        elif len(hex_color) == 6:
            hex_color += "FF"

        # Ensures an 8 characters hex number
        if len(hex_color) == 4:
            hex_color = "".join([c * 2 for c in hex_color])

        # Convert and store the characters
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = int(hex_color[6:8], 16)

        if fmt is None:
            fmt = KColorConverter._determine_format((r, g, b))

        return KColorConverter._format_rgba((r, g, b, a), fmt)

    @staticmethod
    def _rgb_to_hex6(rgb: Tuple[Num, Num, Num]) -> str:
        return "#{:02X}{:02X}{:02X}".format(
            KColorConverter.float_to_int(rgb[0])
            if isinstance(rgb[0], float)
            else rgb[0],
            KColorConverter.float_to_int(rgb[1])
            if isinstance(rgb[1], float)
            else rgb[1],
            KColorConverter.float_to_int(rgb[2])
            if isinstance(rgb[2], float)
            else rgb[2],
        )

    @staticmethod
    def _rgba_to_hex8(
        rgba: Union[Tuple[Num, Num, Num, Num], Tuple[Num, Num, Num]],
    ) -> str:
        if len(rgba) == 3:
            rgba = (*rgba, 255)  # Adds an alpha value of 255

        return "#{:02X}{:02X}{:02X}{:02X}".format(
            KColorConverter.float_to_int(rgba[0])
            if isinstance(rgba[0], float)
            else rgba[0],
            KColorConverter.float_to_int(rgba[1])
            if isinstance(rgba[1], float)
            else rgba[1],
            KColorConverter.float_to_int(rgba[2])
            if isinstance(rgba[2], float)
            else rgba[2],
            KColorConverter.float_to_int(rgba[3])
            if isinstance(rgba[3], float)
            else rgba[3],
        )

    @staticmethod
    def _format_rgb(
        rgb: Tuple[Num, Num, Num], fmt: Optional[str]
    ) -> Tuple[Num, Num, Num]:
        if fmt is None:
            fmt = KColorConverter._determine_format(rgb)

        if any(char not in {"I", "F"} for char in fmt):
            raise ValueError("The format can only be composed of 'I' or 'F'")

        def get_type(conversion_char):
            return int if conversion_char == "I" else float

        def convert_value(value, target_type):
            if isinstance(value, target_type):
                return value
            return (
                KColorConverter.float_to_int(value)
                if target_type == int
                else KColorConverter.int_to_float(value)
            )

        format_length = len(fmt)
        if format_length == 1:
            r_type = g_type = b_type = get_type(fmt[0])
        elif format_length == 3:
            r_type = get_type(fmt[0])
            g_type = get_type(fmt[1])
            b_type = get_type(fmt[2])
        else:
            raise ValueError("Format string length must be 1 or 3")

        converted_values = (
            convert_value(rgb[0], r_type),
            convert_value(rgb[1], g_type),
            convert_value(rgb[2], b_type),
        )

        return converted_values

    @staticmethod
    def _format_rgba(
        rgba: Union[Tuple[Num, Num, Num, Num], Tuple[Num, Num, Num]],
        fmt: Optional[str],
    ) -> Tuple[Num, Num, Num, Num]:
        if len(rgba) == 3:
            rgba = (*rgba, 255)  # Adds an alpha value of 255

        if fmt is None:
            fmt = KColorConverter._determine_format(rgba)

        if any(char not in {"I", "F"} for char in fmt):
            raise ValueError("The format can only be composed of 'I' or 'F'")

        def get_type(conversion_char):
            return int if conversion_char == "I" else float

        def convert_value(value, target_type):
            if isinstance(value, target_type):
                return value
            return (
                KColorConverter.float_to_int(value)
                if target_type == int
                else KColorConverter.int_to_float(value)
            )

        format_length = len(fmt)
        if format_length == 1:
            r_type = g_type = b_type = a_type = get_type(fmt[0])
        elif format_length == 2:
            r_type = g_type = b_type = get_type(fmt[0])
            a_type = get_type(fmt[1])
        elif format_length == 3:
            r_type = get_type(fmt[0])
            g_type = get_type(fmt[1])
            b_type = get_type(fmt[2])
            a_type = float if isinstance(rgba[3], float) else int
        elif format_length == 4:
            r_type = get_type(fmt[0])
            g_type = get_type(fmt[1])
            b_type = get_type(fmt[2])
            a_type = get_type(fmt[3])
        else:
            raise ValueError("Format string length must be between 1 and 4")

        converted_values = (
            convert_value(rgba[0], r_type),
            convert_value(rgba[1], g_type),
            convert_value(rgba[2], b_type),
            convert_value(rgba[3], a_type),
        )

        return converted_values

    @classmethod
    def _to_rgb(
        cls,
        color: Union[str, Tuple[Num, Num, Num], Tuple[Num, Num, Num, Num]],
        fmt: Optional[str] = None,
    ) -> Tuple[Num, Num, Num]:
        if isinstance(color, Tuple):
            if len(color) == 3:
                return color
            elif len(color) == 4:
                return color[:3]
            else:
                e = "La longitud de las tuplas solo puede ser 3(rgb) o 4(rgba)"
                raise ValueError(e)

        color = cls._hex_to_rgb(color, fmt)
        return cls._format_rgb(color, fmt)

    @classmethod
    def _to_rgba(
        cls,
        color: Union[str, Tuple[Num, Num, Num], Tuple[Num, Num, Num, Num]],
        fmt: Optional[str] = None,
    ) -> Tuple[Num, Num, Num, Num]:
        if isinstance(color, Tuple):
            if len(color) == 3:
                return (*color, 255)
            elif len(color) == 4:
                return color
            else:
                e = "La longitud de las tuplas solo puede ser 3(rgb) o 4(rgba)"
                raise ValueError(e)

        color = cls._hex_to_rgba(color, fmt)
        return cls._format_rgba(color, fmt)

    @classmethod
    def _to_hex6(
        cls, color: Union[str, Tuple[Num, Num, Num], Tuple[Num, Num, Num, Num]]
    ) -> str:
        if isinstance(color, Tuple) and len(color) == 4:
            color = color[:3]
        if isinstance(color, str):
            color = cls._hex_to_rgb(color)
        elif len(color) != 3:
            raise ValueError("HEX6 requiere una tupla de 3 valores")
        return cls._rgb_to_hex6(color)

    @classmethod
    def _to_hex8(
        cls,
        color: Union[str, Tuple[Num, Num, Num, Num], Tuple[Num, Num, Num]],
    ) -> str:
        if isinstance(color, str):
            color = cls._hex_to_rgba(color)
        elif len(color) == 3:
            color = (*color, 255)  # Add alpha value of 255 if not provided
        elif len(color) != 4:
            raise ValueError(
                "HEX8 requiere una tupla de 4 valores o 3 valores más un alpha por defecto"
            )
        return cls._rgba_to_hex8(color)
