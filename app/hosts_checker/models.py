import enum
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
    rtt: Union[float, None]
    port_status: str
    timestamp: datetime


class MessagesEnum:
    PORT_OPENED = "opened"
    PORT_NOT_OPENED = "not opened"
    OK = "ok"
    NETWORK_IS_UNAVAILABLE = "network is unavailable"
    REQUEST_TIMED_OUT = "request timed out"
    DNS_SUCCEED = "dns successfully resolved {}"
    DNS_FAILED = "dns failed to resolve {}"
