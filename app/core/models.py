import enum
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Union


@dataclass
class BaseAnswer:
    success: bool
    message: str
    domain_name: str
    timestamp: datetime

    def to_dict(self):
        return self.__dict__

    def to_string(self):
        return f"{self.timestamp} | {int(self.success)} | {self.domain_name:32} | {self.message:32}"


@dataclass
class ResolvingAnswer(BaseAnswer):
    hosts: List[str] = field(default_factory=list)


@dataclass
class PingAnswer(BaseAnswer):
    host: str
    port: Union[str, int]
    rtt: Union[float, None]
    port_status: str
    domain_name: str

    def to_string(self):
        base_str = super(PingAnswer, self).to_string()

        return f'{base_str} | {self.host:15} | {self.port:6} | {round(self.rtt, 2):8} | {self.port_status}'


class MessagesEnum:
    PORT_OPENED = "opened"
    PORT_NOT_OPENED = "not opened"
    OK = "ok"
    NETWORK_IS_UNAVAILABLE = "network is unavailable"
    REQUEST_TIMED_OUT = "request timed out"
    DNS_SUCCEED = "resolved"
    DNS_FAILED = "failed to resolve"


class HostType(enum.Enum):
    IP = "ip"
    DOMAIN_NAME = "domain name"


@dataclass
class HostInfo:
    host: str
    ports: List = field(default_factory=list)
    type: HostType = None

    def __post_init__(self):
        if re.fullmatch(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", self.host):
            self.type = HostType.IP
        else:
            self.type = HostType.DOMAIN_NAME


@dataclass
class HTTPResponse:
    status_code: int
