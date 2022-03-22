import os
import socket
import sqlite3

from datetime import datetime

from ChatApp.exceptions import InvalidIpException, InvalidPortException
from ChatApp.settings import DB_PATH, PORT_MAX, PORT_MIN


def check_path(path):
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def get_conn():
    check_path(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory

    return conn


def check_ip(ip):
    # if not is_valid_ip(ip):
    try:
        ip = socket.gethostbyname(ip)
        return ip
    except socket.gaierror:
        raise InvalidIpException

# def is_valid_ip(ip: str):
#     nums = ip.split(".")
#     if len(nums) != 4:
#         return False
#     return all(map(lambda x: 0 <= int(x) <= 255, nums))


def check_port(port):
    try:
        port = int(port)
        if not PORT_MIN <= port <= PORT_MAX:
            raise InvalidPortException
    except ValueError:
        raise InvalidPortException

    return port


def get_timestamp():
    return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())


def render_offline_messages(messages):
    template = ">>> {}{}: <{}> {}"
    result = []
    for message in messages:
        is_group = message.get("type_") == "send_all"
        result.append(template.format(
            "Channel Message " if is_group else "",
            message.get("from_"),
            message.get("timestamp"),
            message.get("content")
        ))

    return "\n".join(result)
