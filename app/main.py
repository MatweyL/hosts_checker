import datetime
import pprint
from contextlib import closing
from dataclasses import dataclass, field
import socket
from typing import Tuple, List, Optional, Any, Union

from pythonping import ping
from time import perf_counter, sleep


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
    timestamp: datetime.datetime


@dataclass
class LoggerPingAnswer:
    domain: str
    host: str
    port: Union[str, int]
    rtt: float
    port_status: str
    timestamp: datetime.datetime


def resolve_domain(domain_name: str) -> ResolvingAnswer:
    try:
        domain_info = socket.gethostbyname_ex(domain_name)
        return ResolvingAnswer(success=True, message=f'dns successfully resolved {domain_name}', hosts=domain_info[2])
    except socket.gaierror:
        return ResolvingAnswer(success=False, message=f'dns failed to resolve {domain_name}')


def ping_server(host: str, port: int = None, timeout: float = 2):
    if not port:
        result = ping(host)  # Runtime error: RuntimeError: Cannot resolve address "yandekx1.ru", try verify your DNS or host file
        print(result)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            start_time = perf_counter()
            result = sock.connect_ex((host, port))
            rtt = perf_counter() - start_time
            print('rtt', rtt)
            pprint.pprint(result)



def main():
    import socket

    # conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = 'toster.ru'
    # port = 443
    # conn.connect((host, port))
    #
    # print(conn)
    import socket

    # resolving_answer = resolve_domain("yandeix.ru")
    # if resolving_answer.success:
    #     for ip in resolving_answer.hosts:
    #         print(ip)
    # else:
    #     print(resolving_answer.message)

    r = ping_server("213.86.34.12", 4500)  # 10049 - port is not valid
    print(r)


if __name__ == "__main__":
    main()
