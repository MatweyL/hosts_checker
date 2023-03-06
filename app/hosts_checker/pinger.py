import datetime
import os
import socket
from time import perf_counter

import pythonping

from app.core.models import PingAnswer, MessagesEnum, ResolvingAnswer
from app.logger.loggers import ConsoleLogger, FileLogger
from app.utils.base import get_project_root


def resolve_domain(domain_name: str) -> ResolvingAnswer:
    try:
        domain_info = socket.gethostbyname_ex(domain_name)
        return ResolvingAnswer(success=True, domain_name=domain_name,
                               message=MessagesEnum.DNS_SUCCEED.format(domain_name),
                               hosts=domain_info[2],
                               timestamp=datetime.datetime.now())
    except socket.gaierror:
        return ResolvingAnswer(success=False, domain_name=domain_name,
                               message=MessagesEnum.DNS_FAILED.format(domain_name),
                               timestamp=datetime.datetime.now())


def ping(host: str, port: int = None, domain_name: str = "???", timeout: float = 2, count: int = 4) -> PingAnswer:
    if not port:
        ping_answer = _ping_icmp(host, domain_name, timeout, count)
    else:
        ping_answer = _ping_port(host, port, domain_name, timeout, count)
    ping_answer.domain_name = domain_name
    return ping_answer


def _ping_icmp(host: str, domain_name: str, timeout: float = 2, count: int = 4) -> PingAnswer:
    rtt = None
    success = False
    try:
        response = pythonping.ping(host, timeout=timeout, count=count)
        success = response.success()
        message = MessagesEnum.OK if success else MessagesEnum.REQUEST_TIMED_OUT
        rtt = response.rtt_avg
    except OSError:
        message = MessagesEnum.NETWORK_IS_UNAVAILABLE
    return PingAnswer(success=success, message=message, rtt=rtt * 1000, host=host, port=-1,
                      port_status='???', timestamp=datetime.datetime.now(), domain_name=domain_name)


def _ping_port(host: str, port: int, domain_name: str, timeout: float = 2, count: int = 4) -> PingAnswer:
    successes = 0
    rtt_avg = 0
    error_code = None
    for retry in range(count):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            start_time = perf_counter()
            response_code = sock.connect_ex((host, port))
            rtt = perf_counter() - start_time
            rtt_avg = (retry * rtt_avg + rtt) / (retry + 1)
            if response_code == 0:
                successes += 1
            else:
                error_code = response_code
    success = successes / count >= 0.5
    if error_code == 10065:
        message = MessagesEnum.NETWORK_IS_UNAVAILABLE
    else:
        message = MessagesEnum.OK if success else f'error: {error_code}'
    port_status = MessagesEnum.PORT_OPENED if success else MessagesEnum.PORT_NOT_OPENED
    return PingAnswer(success=success, message=message, rtt=rtt_avg * 1000, host=host, port=port,
                      port_status=port_status, timestamp=datetime.datetime.now(), domain_name=domain_name)


if __name__ == "__main__":
    logger = FileLogger(os.path.join(get_project_root(), "logs"))
    r = ping('5.255.255.115', 80, 'yandex.ru', count=1)
    logger.log(r)
    r = resolve_domain("yandex.ru")

    logger.log(r)
