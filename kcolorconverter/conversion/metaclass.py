import typing_extensions
import warnings
from ..warnings import KColorConverterDeprecatedSince002
from ..constants import N, RGB_TUPLE, RGBA_TUPLE


class KColorConverterMeta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

    @property
    @typing_extensions.deprecated(
        "The `Num` attribute is deprecated and will be removed in a future version. Use N instead.",
        category=None
    )
    def Num(cls):
        warnings.warn(
            message="The `Num` attribute is deprecated and will be removed in a future version. Use N instead.",
            category=KColorConverterDeprecatedSince002,
            stacklevel=2,
        )
        return N

    @property
    def N(cls):
        return N

    @property
    def RGB_TUPLE(cls):
        return RGB_TUPLE

    @property
    def RGBA_TUPLE(cls):
        return RGBA_TUPLE
