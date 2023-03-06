import os

from app.core.models import HostInfo
from app.hosts_checker.checker import HostsChecker
from app.logger.loggers import ConsoleLogger, FileLogger
from app.utils.base import get_project_root


def main():

    console_logger = ConsoleLogger()
    file_logger = FileLogger(os.path.join(get_project_root(), "logs"))
    hosts_checker = HostsChecker([HostInfo(host='yandex.ru', ports=[80, 443]),
                                  HostInfo(host="instagram.com")], timeout=5)
    hosts_checker.register_logger(console_logger)
    hosts_checker.register_logger(file_logger)
    hosts_checker.start()


if __name__ == "__main__":
    main()
