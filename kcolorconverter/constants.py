from typing import TypeAlias, Type, Union, Tuple
from enum import Enum

N = Union[int, float]
RGB_TUPLE = tuple[N, N, N]
RGBA_TUPLE = tuple[N, N, N, N]


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
