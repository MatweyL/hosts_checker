from app.core.models import BaseAnswer
from app.logger import Logger


class ConsoleLogger(Logger):
    def log(self, message: BaseAnswer):
        print(message.to_string())


class FileLogger:
    pass


class DatabaseLogger:
    pass
