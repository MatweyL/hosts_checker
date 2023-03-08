class NetworkConnectionError(Exception):
    pass


class NoSuchFileError(FileNotFoundError):
    def __init__(self, file_path: str):
        super(NoSuchFileError, self).__init__(f"There is no file on path {file_path}")


class WrongInputFormatError(Exception):

    def __init__(self, line_number: int, error_message: str = ""):
        super(WrongInputFormatError, self).__init__(f"line: {line_number}; {error_message}")


class InvalidIpAddressError(WrongInputFormatError):

    def __init__(self, line_number: int, ip: str):
        super(InvalidIpAddressError, self).__init__(line_number, f"Wrong ip address format: {ip}")


class InvalidDomainError(WrongInputFormatError):

    def __init__(self,  line_number: int, domain_name: str):
        super(InvalidDomainError, self).__init__(line_number, f"Wrong domain name format: {domain_name}")


class InvalidPortNumberError(WrongInputFormatError):
    def __init__(self,  line_number: int, port: str | int):
        super(InvalidPortNumberError, self).__init__(line_number, f"Port {port} must be between 1 and 65535")


class InvalidPortFormatError(WrongInputFormatError):
    def __init__(self, line_number: int, port: str | int):
        super(InvalidPortFormatError, self).__init__(line_number,f"Wrong port format: {port}; port must be integer")


class ConfigError(Exception):
    pass


class FieldMissedError(ConfigError):
    def __init__(self, missed_field: str):
        super(FieldMissedError, self).__init__(f"field is missed in config: {missed_field}")


class UnknownLoggerError(ConfigError):
    def __init__(self, logger_name: str):
        super(UnknownLoggerError, self).__init__(f"unknown logger name: {logger_name}")


class UnknownNotifierError(ConfigError):
    def __init__(self, notifier_name: str):
        super(UnknownNotifierError, self).__init__(f"unknown notifier name: {notifier_name}")
