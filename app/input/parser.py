import csv
from typing import List

from app.core.exceptions import NoSuchFileError
from app.core.models import HostInfo
from app.utils.base import get_project_root


def get_hosts_info(file_path: str) -> List[HostInfo]:
    try:
        hosts_info_raw = read(file_path)
    except FileNotFoundError:
        raise NoSuchFileError(f"There is no file on path {file_path}")



def read(file_path: str):
    with open(file_path,  encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';', quotechar="\"")
        return [row for row in csv_reader]


def validate(hosts_info: List) -> List:
    pass


if __name__ == "__main__":
    print(read(fr"{get_project_root()}\hosts.csv"))
