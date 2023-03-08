import os.path
from dataclasses import dataclass, field
from typing import List

from app.core.exceptions import NoSuchFileError


@dataclass
class FileLoggerConfig:
    logs_dir_path: str
    log_file_max_size: int

    def __post_init__(self):
        if self.log_file_max_size <= 0:
            raise ValueError(f"log file max size must be greater than 0, got {self.log_file_max_size}")
        if not os.path.exists(self.logs_dir_path):
            raise NoSuchFileError(self.logs_dir_path)


@dataclass
class TelegramNotifierConfig:
    bot_token: str
    known_users: List[int] = field(default_factory=list)

    def __post_init__(self):
        if len(self.known_users) == 0:
            raise ValueError("Telegram notifier demand users ids for notifying")


@dataclass
class HostsCheckerConfig:
    ping_count: int
    ping_timeout: float
    sleep_timeout: float

    def __post_init__(self):
        if self.ping_count < 1:
            raise ValueError("ping count must be greater than 0")
        if self.ping_timeout <= 1:
            raise ValueError("ping timeout must be greater than 1")
        if self.sleep_timeout < 0:
            raise ValueError("sleep timeout must be non-negative")