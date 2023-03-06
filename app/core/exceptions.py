class NetworkConnectionError(Exception):
    pass


class NoSuchFileError(Exception):
    pass


class WrongInputFormatError(Exception):
    pass


class InvalidIpAddressError(WrongInputFormatError):
    pass


class InvalidDomainError(WrongInputFormatError):
    pass


class InvalidPortError(WrongInputFormatError):
    pass
