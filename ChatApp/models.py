# from enum import Enum

from ChatApp.utils import get_conn

# class Status(Enum):
#     YES = "yes"
#     NO = "no"


class User:

    # @classmethod
    # def new_client(cls, ip, port, client_name, status="yes"):
    #     Client._check_param(ip, port, client_name, status)
    #     return cls(ip, port, client_name, status)

    def __init__(self, name, ip, port, status="yes"):
        self.name = name
        self.ip = ip
        self.port = port
        self.status = status

    @property
    def addr(self):
        return (self.ip, self.port)

    def __repr__(self):
        return f"User({self.name}, {self.addr}, {self.status})"

    # @staticmethod
    # def _check_param(ip, port, client_name, status):
    #     assert isinstance(ip, str)
    #     assert isinstance(port, int)
    #     assert isinstance(client_name, str)
    #     assert isinstance(status, Status)

    #     if not is_valid_ip(ip):
    #         raise InvalidIpException

    #     if not is_valid_port(port):
    #         raise InvalidPortException

    def save(self):
        pass

    @classmethod
    def get_all(cls):
        sql = "select * from user"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        users = []
        for user in result:
            users.append(cls(**user))

        return users

    @classmethod
    def get_by_name(cls, name):
        sql = "select * from user where name=?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (name, ))
        user = cursor.fetchone()
        return cls(**user) if user else None
