from abc import ABCMeta, abstractmethod

from app.core.models import BaseAnswer


class Logger(metaclass=ABCMeta):

    @abstractmethod
    def log(self, message: BaseAnswer):
        raise NotImplementedError
