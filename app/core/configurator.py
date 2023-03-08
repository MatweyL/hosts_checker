import json
from typing import List

from app.core.configs import FileLoggerConfig, TelegramNotifierConfig, HostsCheckerConfig
from app.core.exceptions import NoSuchFileError, FieldMissedError
from app.logger import Logger
from app.logger.loggers import ConsoleLogger, FileLogger
from app.notifier import Notifier
from app.notifier.notifiers import TelegramNotifier


class Configurator:

    def __init__(self, path_to_config: str):
        self.path_to_config = path_to_config
        self.loggers: List[Logger] = []
        self.notifiers: List[Notifier] = []
        self.loggers_mapping = {
            "file": {
                "class": FileLogger,
                "config": FileLoggerConfig,
                "fields": ['log_file_max_size', 'logs_dir_path']
            },
            "console": {
                "class": ConsoleLogger
            }
        }
        self.notifiers_mapping = {
            "telegram": {
                "class": TelegramNotifier,
                "config": TelegramNotifierConfig,
                "fields": ['bot_token', 'known_users']
            }
        }
        self.hosts_checker_config: HostsCheckerConfig = None
        self.hosts_file_path: str = None

    def _load_loggers(self, config: dict):
        for logger_config in config['loggers']:
            logger_name = logger_config["name"]
            if self.loggers_mapping.get(logger_name):
                if self.loggers_mapping[logger_name].get("config"):
                    config_dict = {}
                    try:
                        for field in self.loggers_mapping[logger_name]["fields"]:
                            config_dict[field] = logger_config[field]
                    except KeyError as e:
                        raise FieldMissedError(str(e))
                    config_class = self.loggers_mapping[logger_name]["config"](**config_dict)
                    logger = self.loggers_mapping[logger_name]["class"](config_class)
                else:
                    logger = self.loggers_mapping[logger_name]["class"]()
                self.loggers.append(logger)
            else:
                print(f'warning: no logger with name: {logger_name}')

    def _load_notifiers(self, config: dict):
        for notifier_config in config['notifiers']:
            notifier_name = notifier_config["name"]
            if self.notifiers_mapping.get(notifier_name):
                if self.notifiers_mapping[notifier_name].get("config"):
                    config_dict = {}
                    try:
                        for field in self.notifiers_mapping[notifier_name]["fields"]:
                            config_dict[field] = notifier_config[field]
                    except KeyError as e:
                        raise FieldMissedError(str(e))
                    config_class = self.notifiers_mapping[notifier_name]["config"](**config_dict)
                    notifier = self.notifiers_mapping[notifier_name]["class"](config_class)
                else:
                    notifier = self.notifiers_mapping[notifier_name]["class"]()
                self.notifiers.append(notifier)
            else:
                print(f'warning: no notifier with name: {notifier_name}')

    def _load_hosts_checker_config(self, config: dict):
        if config.get("hosts_checker"):
            hosts_checker_config = config["hosts_checker"]
            try:
                self.hosts_checker_config = HostsCheckerConfig(ping_count=hosts_checker_config['ping_count'],
                                                               ping_timeout=hosts_checker_config['ping_timeout'],
                                                               sleep_timeout=hosts_checker_config['sleep_timeout'])
            except KeyError as e:
                raise FieldMissedError(str(e))
        else:
            raise FieldMissedError("hosts_checker")

    def _load_hosts_file_path(self, config: dict):
        try:
            self.hosts_file_path = config['hosts_file_path']
        except KeyError as e:
            raise FieldMissedError(str(e))

    def bootstrap(self):
        try:
            with open(self.path_to_config) as json_file:
                config = json.load(json_file)
        except FileNotFoundError:
            raise NoSuchFileError(file_path=self.path_to_config)
        self._load_loggers(config)
        self._load_notifiers(config)
        self._load_hosts_checker_config(config)

    def get_notifiers(self):
        return self.notifiers

    def get_loggers(self):
        return self.loggers

    def get_hosts_checker_config(self):
        return self.hosts_checker_config
