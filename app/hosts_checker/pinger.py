import abc
import datetime
import errno
import socket
from time import perf_counter

from pythonping import ping

from app.hosts_checker.models import PingAnswer


def ping_icmp(host: str, timeout: float = 2, count: int = 4):
    rtt = None
    success = False
    try:
        response = ping(host, timeout=timeout, count=count)
        success = response.success()
        message = 'ok' if success else 'request timed out'
        rtt = response.rtt_avg
    except OSError:
        message = 'network is not available'
    return PingAnswer(success=success, message=message, rtt=rtt * 1000, host=host, port=-1,
                      port_status='???', timestamp=datetime.datetime.now())


def ping_port(host: str, port: int, timeout: float = 2, count: int = 4):
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
    port_status = "opened" if success else "not opened"
    message = 'ok' if success else error_code
    return PingAnswer(success=success, message=message, rtt=rtt_avg * 1000, host=host, port=port,
                      port_status=port_status, timestamp=datetime.datetime.now())


if __name__ == "__main__":
    r = ping_port('yandex.ru', 80)
    print(r)
