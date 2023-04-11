import datetime
import socket
import ssl

from app.core.models import SSLCertificateCheckAnswer, MessagesEnum
from app.hosts_checker.pinger import resolve_domain


def check_certificate(host: str, port: int) -> SSLCertificateCheckAnswer:
    success = True
    message = MessagesEnum.SSL_CERTIFICATE_VALID
    try:
        context = ssl.create_default_context()

        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host):
                pass
    except socket.gaierror:
        success = False
        message = MessagesEnum.SSL_NETWORK_IS_UNAVAILABLE
    except ConnectionRefusedError:
        success = False
        message = MessagesEnum.SSL_CLOSED_PORT.format(port)
    except ssl.SSLCertVerificationError:
        success = False
        message = MessagesEnum.SSL_CERTIFICATE_WRONG
    except ssl.SSLError as e:
        success = False
        message = e.reason
    return SSLCertificateCheckAnswer(success=success,
                                     domain_name=host,
                                     message=message,
                                     timestamp=datetime.datetime.now())


if __name__ == "__main__":
    hosts = resolve_domain('ya.ru').hosts
    print(check_certificate('ya.ru', 443))
    for host in hosts:
        print(check_certificate(host, 443))