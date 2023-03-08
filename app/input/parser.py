import csv
import os.path
import re
from typing import List

from app.core.exceptions import NoSuchFileError, InvalidDomainError, InvalidIpAddressError, InvalidPortNumberError, \
    InvalidPortFormatError
from app.core.models import HostInfo
from app.utils.base import get_project_root


def get_hosts_info(file_path: str) -> List[HostInfo]:
    try:
        hosts_info_raw = read(file_path)
        return validate(hosts_info_raw)
    except FileNotFoundError:
        raise NoSuchFileError(file_path)


def read(file_path: str):
    with open(file_path,  encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';', quotechar="\"")
        return [row for row in csv_reader][1:]


def is_valid_domain_name(domain_name: str):
    res = re.fullmatch("((?=[a-z0-9-]{1,63}\\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\\.)+[a-z]{2,63}", domain_name) or "localhost" in domain_name
    return res


def is_ip(ip: str):
    res = re.fullmatch(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", ip)
    return res is not None


def is_valid_ip(ip: str):
    return re.fullmatch(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", ip) is not None


def validate(hosts_info_raw: List[List[str]]) -> List[HostInfo]:
    hosts_info = []
    line_number = 1
    for host_info_raw in hosts_info_raw:
        line_number += 1
        host = host_info_raw[0]
        ports_raw: List[str] = list(filter(lambda m: m != '', host_info_raw[1].split(',')))
        if is_ip(host):
            if not is_valid_ip(host):
                raise InvalidIpAddressError(line_number, host)
        elif not is_valid_domain_name(host):
            raise InvalidDomainError(line_number, host)
        ports = []
        for port_raw in ports_raw:
            if port_raw.isdigit():
                if 1 < int(port_raw) < 65535:
                    ports.append(int(port_raw))
                else:
                    raise InvalidPortNumberError(line_number, port_raw)
            else:
                raise InvalidPortFormatError(line_number, port_raw)
        hosts_info.append(HostInfo(host=host, ports=ports))
    return hosts_info


if __name__ == "__main__":
    hosts_info_raw = read(fr"{get_project_root()}\hosts.csv")
    print(validate(hosts_info_raw))
