import os

from app.core.exceptions import WrongInputFormatError, NoSuchFileError
from app.core.models import HostInfo
from app.hosts_checker.checker import HostsChecker
from app.input.parser import get_hosts_info
from app.logger.loggers import ConsoleLogger, FileLogger
from app.utils.base import get_project_root


def main():
    try:
        hosts_info = get_hosts_info(file_path="/logs")
    except (WrongInputFormatError, NoSuchFileError) as e:
        print(e)
    else:
        console_logger = ConsoleLogger()
        file_logger = FileLogger(os.path.join(get_project_root(), "logs"))
        hosts_checker = HostsChecker(hosts_info, timeout=5)
        hosts_checker.register_logger(console_logger)
        hosts_checker.register_logger(file_logger)
        hosts_checker.start()


if __name__ == "__main__":
    main()
