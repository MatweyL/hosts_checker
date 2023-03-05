import enum
import re
from dataclasses import dataclass, field
from typing import List


class HostType(enum.Enum):
    IP = "ip"
    DOMAIN_NAME = "domain name"


@dataclass
class HostInfo:
    host: str
    ports: List = field(default=list)
    type: HostType = None

    def __post_init__(self):
        if re.fullmatch(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", self.host):
            self.type = HostType.IP
        else:
            self.type = HostType.DOMAIN_NAME
