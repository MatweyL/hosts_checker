import datetime
import os.path

from app.core.configs import FileLoggerConfig
from app.core.models import BaseAnswer
from app.logger import Logger


class ConsoleLogger(Logger):
    def log(self, message: BaseAnswer):
        print(message.to_string())


class FileLogger(Logger):

    def __init__(self, config: FileLoggerConfig):
        self.config: FileLoggerConfig = config
        self.log_file = None
        self._setup()

    def _setup(self):
        if not os.path.exists(self.config.logs_dir_path):
            os.mkdir(self.config.logs_dir_path)
        log_files = [file for file in os.listdir(self.config.logs_dir_path) if ".log" in file]
        if log_files:
            last_log = max(log_files)
            self.log_file = os.path.join(self.config.logs_dir_path, last_log)
            self._check_log_file_size()
        else:
            self._update_log_file()

    def _check_log_file_size(self):
        if os.path.getsize(self.log_file) > self.config.log_file_max_size:
            self._update_log_file()

    def _update_log_file(self):
        self.log_file = os.path.join(self.config.logs_dir_path, f'{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log')

    def log(self, message: BaseAnswer):
        with open(self.log_file, "a") as log_file:
            log_file.write(f'{message.to_string()}\n')
        self._check_log_file_size()


class DatabaseLogger:
    pass
