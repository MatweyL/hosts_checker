import datetime
import os.path
from typing import List

from app.core.models import BaseAnswer
from app.logger import Logger


class ConsoleLogger(Logger):
    def log(self, message: BaseAnswer):
        print(message.to_string())


class FileLogger(Logger):

    def __init__(self, logs_path: str):
        self.logs_dir_path: str = logs_path
        self.log_file = None
        self.messages: List[BaseAnswer] = []
        self.messages_max_len = 10
        self.log_file_max_size = 1024 * 1024 * 100  # 100MB
        self._setup()

    def _setup(self):
        if not os.path.exists(self.logs_dir_path):
            os.mkdir(self.logs_dir_path)
        log_files = [file for file in os.listdir(self.logs_dir_path) if ".log" in file]
        if log_files:
            last_log = max(log_files)
            self.log_file = os.path.join(self.logs_dir_path, last_log)
            self._check_log_file_size()
        else:
            self._update_log_file()

    def _check_log_file_size(self):
        if os.path.getsize(self.log_file) > self.log_file_max_size:
            self._update_log_file()

    def _update_log_file(self):
        self.log_file = os.path.join(self.logs_dir_path, f'{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log')

    def log(self, message: BaseAnswer):
        self.messages.append(message)
        if len(self.messages) > self.messages_max_len:
            with open(self.log_file, "a") as log_file:
                for message in self.messages:
                    log_file.write(f'{message.to_string()}\n')
        self._check_log_file_size()


class DatabaseLogger:
    pass
