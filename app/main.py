import os
import sys

from app.core.configurator import Configurator
from app.core.exceptions import WrongInputFormatError, NoSuchFileError, ConfigError
from app.hosts_checker.checker import HostsChecker
from app.input.parser import get_hosts_info
from app.utils.base import get_project_root


def main():
    try:
        configurator = Configurator(os.path.join(get_project_root(), "config.json"))
        configurator.bootstrap()
    except (ConfigError, NoSuchFileError) as e:
        print(e)
        sys.exit()
    try:
        hosts_info = get_hosts_info(file_path=os.path.join(get_project_root(), "hosts.csv"))
    except (WrongInputFormatError, NoSuchFileError) as e:
        print(e)
        sys.exit()
    hosts_checker = HostsChecker(hosts_info, configurator.get_hosts_checker_config())
    for logger in configurator.get_loggers():
        hosts_checker.register_logger(logger)
    for notifier in configurator.get_notifiers():
        hosts_checker.register_notifier(notifier)
    hosts_checker.start()


if __name__ == "__main__":
    main()
