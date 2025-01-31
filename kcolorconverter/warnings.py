class KColorConverterDeprecationWarning(DeprecationWarning):
    message: str
    since: tuple[int, int, int]
    expected_removal: tuple[int, int, int]

    def __init__(
            self, message: str, *args: object,
            since: tuple[int, int, int], expected_removal: tuple[int, int, int] | None = None
    ) -> None:
        super().__init__(message, *args)
        self.message = message.rstrip('.')
        self.since = since
        self.expected_removal = expected_removal if expected_removal is not None else (since[0] + 1, 0, 0)

    def __str__(self) -> str:
        message = (
            f'{self.message}. Deprecated in KColorConverter v{self.__short_version(self.since)}'
            f' to be removed in V{self.__short_version(self.expected_removal)}'
        )
        return message

    @staticmethod
    def __short_version(version: tuple[int, int, int]) -> str:
        version = f"{version[0]}.{version[1]}"
        return version + f"{version[1]}" if version[1] else version


class KColorConverterDeprecatedSince002(KColorConverterDeprecationWarning):
    """A specific `KColorConverterDeprecation` subclass defining functionality deprecated since 0.0.2"""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args, since=(0, 0, 2))
