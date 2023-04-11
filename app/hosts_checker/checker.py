from time import sleep
from typing import List

from app.core.configs import HostsCheckerConfig
from app.core.models import HostInfo, HostType
from app.hosts_checker.certificates_checker import check_certificate
from app.hosts_checker.pinger import resolve_domain, ping
from app.logger import Logger
from app.notifier import Notifier


class HostsChecker:

    def __init__(self, hosts_info: List[HostInfo], config: HostsCheckerConfig):
        self.hosts_info: List[HostInfo] = hosts_info
        self.config: HostsCheckerConfig = config
        self.loggers: List[Logger] = []
        self.notifiers: List[Notifier] = []

    def register_logger(self, logger: Logger):
        self.loggers.append(logger)

    def register_notifier(self, notifier: Notifier):
        self.notifiers.append(notifier)

    def log(self, message):
        for logger in self.loggers:
            logger.log(message)

    def notify(self, message):
        for notifiers in self.notifiers:
            notifiers.notify(message)

    def ping(self, host: str, port: int = None, domain_name: str = "???"):
        ping_answer = ping(host, port, domain_name, timeout=self.config.ping_timeout, count=self.config.ping_count)
        self.log(ping_answer)
        if not ping_answer.success:
            self.notify(ping_answer)

    def start(self):
        while True:
            for host_info in self.hosts_info:
                if host_info.type == HostType.DOMAIN_NAME:
                    resolving_answer = resolve_domain(host_info.host)
                    self.log(resolving_answer)
                    if not resolving_answer.success:
                        self.notify(resolving_answer)
                        continue
                    hosts = resolving_answer.hosts
                else:
                    hosts = [host_info.host]
                ports = host_info.ports if host_info.ports else [None]

                domain_name = host_info.host if host_info.type == HostType.DOMAIN_NAME else "???"
                for host in hosts:
                    for port in ports:
                        self.ping(host, port, domain_name)

                if 443 in ports:
                    certificate_check_answer = check_certificate(domain_name, 443)
                    self.log(certificate_check_answer)
                    if not certificate_check_answer.success:
                        self.notify(certificate_check_answer)

            sleep(self.config.sleep_timeout)
