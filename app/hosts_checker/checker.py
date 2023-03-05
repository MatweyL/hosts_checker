from time import sleep
from typing import List

from app.core.models import HostInfo, HostType


class HostsChecker:

    def __init__(self, hosts_info: List[HostInfo], timeout: float = 0.1):
        self.hosts_info: List[HostInfo] = hosts_info
        self.timeout = timeout
        self.loggers: List = []
        self.notifiers: List = []

    def register_logger(self, logger):
        self.loggers.append(logger)

    def log(self, message):
        for logger in self.loggers:
            logger.log(message)

    def register_notifier(self, notifier):
        self.notifiers.append(notifier)

    def notify(self, message):
        for notifiers in self.notifiers:
            notifiers.notify(message)

    def start(self):
        while True:
            for host_info in self.hosts_info:
                if host_info.type == HostType.DOMAIN_NAME:
                    pass

            sleep(self.timeout)
