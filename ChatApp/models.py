from enum import Enum

from ChatApp.utils import get_conn
from exceptions import InvalidIpException, InvalidPortException
from utils import is_valid_ip, is_valid_port


class Status(Enum):
    YES = "yes"
    NO = "no"

class Client:
    @classmethod
    def new_client(cls, ip, port, client_name, status=Status.YES):
        Client._check_param(ip, port, client_name, status)
        return cls(ip, port, client_name, status)

    def __init__(self, ip, port, client_name, status=Status.Yes):
        self.ip = ip
        self.port = port
        self.client_name = client_name
        self.status = status

    @staticmethod
    def _check_param(ip, port, client_name, status):
        assert isinstance(ip, str)
        assert isinstance(port, int)
        assert isinstance(client_name, str)
        assert isinstance(status, Status)

        if not is_valid_ip(ip):
            raise InvalidIpException

        if not is_valid_port(port):
            raise InvalidPortException

    def save(self):
        pass

