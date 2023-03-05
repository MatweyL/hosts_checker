import datetime
import socket
from time import perf_counter

import pythonping

from app.hosts_checker.models import PingAnswer, MessagesEnum, ResolvingAnswer


def resolve_domain(domain_name: str) -> ResolvingAnswer:
    try:
        domain_info = socket.gethostbyname_ex(domain_name)
        return ResolvingAnswer(success=True, message=MessagesEnum.DNS_SUCCEED.format(domain_name), hosts=domain_info[2])
    except socket.gaierror:
        return ResolvingAnswer(success=False, message=MessagesEnum.DNS_FAILED.format(domain_name))


def ping(host: str, port: int = None, timeout: float = 2, count: int = 4) -> PingAnswer:
    if not port:
        return _ping_icmp(host, timeout, count)
    return _ping_port(host, port, timeout, count)


def _ping_icmp(host: str, timeout: float = 2, count: int = 4) -> PingAnswer:
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
                      port_status='???', timestamp=datetime.datetime.now())


def _ping_port(host: str, port: int, timeout: float = 2, count: int = 4) -> PingAnswer:
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
        message = MessagesEnum.OK if success else error_code
    port_status = MessagesEnum.PORT_OPENED if success else MessagesEnum.PORT_NOT_OPENED
    return PingAnswer(success=success, message=message, rtt=rtt_avg * 1000, host=host, port=port,
                      port_status=port_status, timestamp=datetime.datetime.now())


if __name__ == "__main__":
    r = _ping_port('yandex.ru', 80)
    print(r)
