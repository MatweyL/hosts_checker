from abc import ABCMeta, abstractmethod

from app.core.models import BaseAnswer


class Notifier(metaclass=ABCMeta):

    @abstractmethod
    def notify(self, message: BaseAnswer):
        raise NotImplementedError
