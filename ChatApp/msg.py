import json
from enum import Enum
from typing import ByteString

# from ChatApp import settings
from ChatApp.models import User


class MsgType(str, Enum):
    CREATE = "create"
    CREATED = "created"
    REG = "reg"
    UPDATE_TABLE = "update_table"
    SEND = "send"
    ACK = "ack"
    SEND_ALL = "send_all"
    SEND_ALL_ACK = "send_all_ack"
    STORE = "store"


class Msg:
    server_addr = None
    name = None

    def __init__(self,
                 content="",
                 type_=None,
                 from_="",
                 to="",
                 to_server=False,
                 addr=None):
        self.content = content
        self.type_ = type_
        self.from_ = from_ or self.name
        self.to = to
        self.to_server = to_server
        self.addr = addr

    @classmethod
    def from_input(cls, user_input, **kwargs):
        words = user_input.split()
        msg = Msg()
        msg.type_ = MsgType(words.pop(0))
        if msg.type_ == MsgType.SEND:
            msg.to = words.pop(0)
        elif msg.type_ == MsgType.REG:
            msg.to_server = True
        elif msg.type_ == MsgType.CREATE:
            msg.to_server = True
        elif msg.type_ == MsgType.SEND_ALL:
            msg.to_server = True
        msg.content = " ".join(words)

        for k, v in kwargs:
            setattr(msg, k, v)

        return msg

    def send(self, socket, **kwargs):
        if self.addr:
            addr = self.addr
        elif self.to_server:
            addr = self.server_addr
        elif self.to:
            user = User.get_by_name(self.to)
            addr = user.addr

        for k, v in kwargs:
            setattr(self, k, v)

        socket.sendto(self.pack(), addr)
    
    def get_receiver_list(self):
        users = User.get_all()
        from_ = self.from_

        receivers = [u.get("name") for u in users if u.get("name") != from_]

        return receivers

    def pack(self):
        return json.dumps(self.__dict__).encode()

    @classmethod
    def unpack(cls, msg: ByteString):
        msg = json.loads(msg.decode())
        return Msg(**msg)
    
