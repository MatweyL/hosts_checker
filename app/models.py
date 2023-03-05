from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Union


@dataclass
class BaseAnswer:
    success: bool
    message: str

    def dict(self):
        return self.__dict__


@dataclass
class ResolvingAnswer(BaseAnswer):
    hosts: List[str] = field(default_factory=list)


@dataclass
class PingAnswer(BaseAnswer):
    host: str
    port: Union[str, int]
    rtt: float
    port_status: str
    timestamp: datetime


@dataclass
class LoggerPingAnswer(PingAnswer):
    domain: str


@dataclass
class LoggerResolvingAnswer(ResolvingAnswer):
    pass
