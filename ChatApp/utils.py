import json
import os
import sqlite3
import sys

from ChatApp.constants import DB_PATH, PORT_MAX, PORT_MIN


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


def is_valid_ip(ip: str):
    nums = ip.split(".")
    if len(nums) != 4:
        return False
    return all(map(lambda x: 0 <= int(x) <= 255, nums))


def is_valid_port(port: int):
    if not isinstance(port, int):
        return False
    return PORT_MIN <= port <= PORT_MAX


def pack_message(msg, **kwargs):
    kwargs["msg"] = msg
    return json.dumps(kwargs).encode()


def unpack_message(rcv_msg):
    return json.loads(rcv_msg.decode())


def show_message(msg):
    sys.stdout.write("\r" + "[re]\n")
    sys.stdout.write("\r" + ">>> ")
