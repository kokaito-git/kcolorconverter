from typing import cast, Type
from .metaclass import KColorConverterMeta
from ..constants import N, RGB_TUPLE, RGBA_TUPLE
from ..constants import KColorFormat


class KColorConverter(metaclass=KColorConverterMeta):
    @classmethod
    def convert(
            cls,
            color: str | RGB_TUPLE | RGBA_TUPLE,
            output_type: KColorFormat = KColorFormat.RGB,
            fmt: str | None = None,
    ) -> str | RGB_TUPLE | RGBA_TUPLE:
        """
        Converts the given color to the specified output type (RGB, RGBA, HEX6, HEX8).
        The input color can be a string (HEX format) or a tuple (RGB or RGBA format).
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
        """ Converts an integer (0 to 255) to a float (0.0 to 1.0). """
        if not isinstance(value, int):
            raise TypeError(f"Se esperaba un valor de tipo int pero se recibió un {type(value).__name__}.")

        if not (0 <= value <= 255):
            raise ValueError("El valor debe estar entre 0 y 255.")
        return value / 255.0

    @staticmethod
    def float_to_int(value: float) -> int:
        """ Converts a float (0.0 to 1.0) to an integer (0 to 255). """
        if not isinstance(value, float):
            raise TypeError(f"Se esperaba un valor de tipo float pero se recibió un {type(value).__name__}.")

        if not (0.0 <= value <= 1.0):
            raise ValueError("El valor debe estar entre 0.0 y 1.0.")
        return round(value * 255)

    """ Main Internal Methods Helpers """

    @staticmethod
    def _read_format(values: tuple[N, ...]) -> str:
        """ Determines the format string (I for int, F for float) for a given tuple of values. """
        format_chars = ""
        for idx, value in enumerate(values):
            if isinstance(value, int):
                format_chars += "I"
            elif isinstance(value, float):
                format_chars += "F"
            else:
                raise ValueError(f"Unsupported value type at index {idx}: {values}.")
        return format_chars

    @classmethod
    def _hex_to_rgb(cls, hex_color: str, fmt: str | None = None) -> RGB_TUPLE:
        """ Converts a hex color (3, 4, 6, or 8 characters) to an RGB tuple. """
        # Adaptamos valores/cogemos por defecto
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        # Válidamos la lóngitud del color
        valid = [3, 4, 6, 8]
        if len(hex_color) not in valid:
            valid_str = ", ".join(map(str, valid))
            raise ValueError(
                f"El color hexadecimal debe tener '{valid_str}' carácteres pero tiene '{len(hex_color)}: {hex_color}"
            )

        # Ensures an 6 characters hex number
        if len(hex_color) == 3:
            hex_color = "".join((c * 2 for c in hex_color))
        elif len(hex_color) == 4:
            hex_color = hex_color[:3]
            hex_color = "".join((c * 2 for c in hex_color))
        elif len(hex_color) == 8:
            hex_color = hex_color[:6]

        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        fmt = cls._read_format((r, g, b)) if fmt is None else fmt
        return KColorConverter._format_rgb((r, g, b), fmt)

    @classmethod
    def _hex_to_rgba(cls, hex_color: str, fmt: str | None = None) -> RGBA_TUPLE:
        """ Converts a hex color (3, 4, 6 or 8 characters) to an RGBA tuple. """
        # Adaptamos valores/cogemos por defecto
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        # Válidamos la lóngitud del color
        valid = [3, 4, 6, 8]
        if len(hex_color) not in valid:
            valid_str = ", ".join(map(str, valid))
            raise ValueError(f"El color hexadecimal debe tener '{valid_str}' caracteres.")

        # Ensures an 8 characters hex number
        if len(hex_color) == 3:
            hex_color = "".join((c * 2 for c in hex_color)) + "FF"
        elif len(hex_color) == 4:
            hex_color = "".join([c * 2 for c in hex_color])
        elif len(hex_color) == 6:
            hex_color += "FF"

        r, g, b, a = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16), int(hex_color[6:8], 16)
        fmt = cls._read_format((r, g, b, a)) if fmt is None else fmt

        return KColorConverter._format_rgba((r, g, b, a), fmt)

    @classmethod
    def _rgb_to_hex6(cls, rgb: RGB_TUPLE) -> str:
        """ Converts an RGB tuple to a hex color string (6 characters). """
        to_int = cls.__n_to_int  # función auxiliar
        return "#{:02X}{:02X}{:02X}".format(to_int(rgb[0]), to_int(rgb[1]), to_int(rgb[2]))

    @classmethod
    def _rgba_to_hex8(cls, rgba: RGBA_TUPLE) -> str:
        """ Converts an RGBA tuple to a hex color string (8 characters) """
        to_int = cls.__n_to_int  # función auxiliar
        return "#{:02X}{:02X}{:02X}{:02X}".format(
            to_int(rgba[0]), to_int(rgba[1]), to_int(rgba[2]), to_int(rgba[3])
        )

    @classmethod
    def _format_rgb(cls, rgb: RGB_TUPLE, fmt: str | None) -> RGB_TUPLE:
        """ Formats the RGB tuple according to the specified format (either int or float). """
        if fmt is None:
            fmt = KColorConverter._read_format(rgb)
        else:
            if any(char not in {"I", "F"} for char in fmt):
                raise ValueError("The format can only be composed of 'I' or 'F'")

        format_length = len(fmt)
        if format_length in [1, 2]:
            r_type = g_type = b_type = cls.__get_fmt_type_from_char(fmt[0])
        elif format_length in [3, 4]:  # ignoramos el alpha pero lo permitimos
            r_type = cls.__get_fmt_type_from_char(fmt[0])
            g_type = cls.__get_fmt_type_from_char(fmt[1])
            b_type = cls.__get_fmt_type_from_char(fmt[2])
        else:
            raise ValueError(
                "Format string length must be 1 or 3 (it could be 2, 4 but alpha format will be ignored): "
                f"length was {format_length}."
            )

        converted_values = (
            cls.__apply_fmt_by_type(rgb[0], r_type),
            cls.__apply_fmt_by_type(rgb[1], g_type),
            cls.__apply_fmt_by_type(rgb[2], b_type),
        )

        return converted_values

    @classmethod
    def _format_rgba(cls, rgba: RGBA_TUPLE, fmt: str | None) -> RGBA_TUPLE:
        """ Formats the RGBA tuple according to the specified format (either int or float). """
        if fmt is None:
            fmt = KColorConverter._read_format(rgba)
        else:
            if any(char not in {"I", "F"} for char in fmt):
                raise ValueError("The format can only be composed of 'I' or 'F'")

        format_length = len(fmt)
        if format_length == 1:  # todos igual
            r_type = g_type = b_type = a_type = cls.__get_fmt_type_from_char(fmt[0])
        elif format_length == 2:  # rgb y a diferenciados
            r_type = g_type = b_type = cls.__get_fmt_type_from_char(fmt[0])
            a_type = cls.__get_fmt_type_from_char(fmt[1])
        elif format_length == 4:  # r,g,b,a todos aparte
            r_type = cls.__get_fmt_type_from_char(fmt[0])
            g_type = cls.__get_fmt_type_from_char(fmt[1])
            b_type = cls.__get_fmt_type_from_char(fmt[2])
            a_type = cls.__get_fmt_type_from_char(fmt[3])
        else:
            raise ValueError("Format string length must be 1, 2 or 4.")

        converted_values = (
            cls.__apply_fmt_by_type(rgba[0], r_type),
            cls.__apply_fmt_by_type(rgba[1], g_type),
            cls.__apply_fmt_by_type(rgba[2], b_type),
            cls.__apply_fmt_by_type(rgba[3], a_type),
        )

        return converted_values

    """ Main Internal Methods """

    @classmethod
    def _to_rgb(cls, color: str | RGB_TUPLE | RGBA_TUPLE, fmt: str | None = None, ) -> RGB_TUPLE:
        """ Converts a color to an RGB tuple.  """
        rgb: RGB_TUPLE
        if isinstance(color, tuple):
            if len(color) == 3:
                rgb = color
            elif len(color) == 4:
                rgb = cast(tuple[N, N, N], color[:3])
            else:
                raise ValueError("La longitud de las tuplas solo puede ser 3(rgb) o 4(rgba)")
        elif isinstance(color, str):
            rgb = cls._hex_to_rgb(color, fmt)
        else:
            raise TypeError(f"Típo inválido de color: {type(color).__name__}.")

        return cls._format_rgb(rgb, fmt)

    @classmethod
    def _to_rgba(cls, color: str | RGB_TUPLE | RGBA_TUPLE, fmt: str | None = None) -> RGBA_TUPLE:
        """ Converts a color to an RGBA tuple. """
        # Si el color ya es una tupla, la retornamos
        rgba: RGBA_TUPLE
        if isinstance(color, tuple):
            if len(color) == 3:
                rgba = cast(tuple[N, N, N, N], (*color, 255))
            elif len(color) == 4:
                rgba = color  # ya es una tupla de 4 elementos
            else:
                raise ValueError("La longitud de las tuplas solo puede ser 3 o 4.")
        elif isinstance(color, str):
            rgba = cls._hex_to_rgba(color, fmt)
        else:
            raise TypeError(f"Típo inválido de color: {type(color).__name__}.")

        # Si el color no es una tupla
        return cls._format_rgba(rgba, fmt)

    @classmethod
    def _to_hex6(cls, color: str | RGB_TUPLE | RGBA_TUPLE) -> str:
        """ Converts a color to a hex format (6 characters). """
        rgb: RGB_TUPLE

        if isinstance(color, str):
            rgb_or_rgba = cls._hex_to_rgb(color)
            rgb = cast(RGB_TUPLE, rgb_or_rgba[:3]) if len(rgb_or_rgba) == 4 else rgb_or_rgba
        elif isinstance(color, tuple):
            if len(color) == 3:
                rgb = color
            elif len(color) == 4:
                rgb = cast(RGB_TUPLE, color[:3])
            else:
                raise ValueError("La longitud de las tuplas solo puede ser 3 o 4.")
        else:
            raise TypeError(f"Típo inválido de color: {type(color).__name__}.")

        return cls._rgb_to_hex6(rgb)

    @classmethod
    def _to_hex8(cls, color: str | RGB_TUPLE | RGBA_TUPLE) -> str:
        """ Converts a color to a hex format (8 characters). """
        rgba: RGBA_TUPLE

        if isinstance(color, str):
            rgb_or_rgba = cls._hex_to_rgba(color)
            rgba = cast(RGBA_TUPLE, (*rgb_or_rgba, 255)) if len(rgb_or_rgba) == 3 else rgb_or_rgba
        elif isinstance(color, tuple):
            if len(color) == 3:
                rgba = cast(RGBA_TUPLE, (*color, 255))
            elif len(color) == 4:
                rgba = color
            else:
                raise ValueError("La longitud de las tuplas solo puede ser 3 o 4.")
        else:
            raise TypeError(f"Típo inválido de color: {type(color).__name__}.")

        return cls._rgba_to_hex8(rgba)

    """ Auxiliary Methods """

    @classmethod
    def __n_to_int(cls, value: N) -> int:
        """ Convert a N (float|int) into int (using cls.float_to_int when needed) """
        return value if isinstance(value, int) else cls.float_to_int(value)

    @staticmethod
    def __get_fmt_type_from_char(char: str) -> Type[N]:
        return int if char == "I" else float

    @staticmethod
    def __apply_fmt_by_type(value: N, target_type: Type[N]):
        if isinstance(value, target_type):
            return value
        return KColorConverter.float_to_int(value) if target_type == int else KColorConverter.int_to_float(value)

    @classmethod
    def __apply_fmt_by_char(cls, value: N, fmt_char: str) -> N:
        target_type: Type[N] = cls.__get_fmt_type_from_char(fmt_char)
        return cls.__apply_fmt_by_type(value, target_type)
