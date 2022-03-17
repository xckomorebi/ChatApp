import threading
from socket import *

from ChatApp.models import User
from ChatApp.msg import Msg, MsgType
from ChatApp.settings import TIMEOUT


def send(msg):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    # if msg.type_


def broadcast(msg):
    pass


def server_handle_received_msg(socket, msg, addr):
    rcv_msg = Msg.unpack(msg)
    type_ = rcv_msg.type_
    if type_ == MsgType.CREATE:
        user = User(rcv_msg.from_, addr[0], addr[1])
        user.save_or_update()
        msg = Msg(to=rcv_msg.from_, type_=MsgType.CREATED)
        msg.send(socket)

        msg = Msg(content=User.get_all,
                  type_=MsgType.UPDATE_TABLE,
                  from_=rcv_msg.from_)

        broadcast(msg) # TODO


def server_main(port: int):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", port))

    while True:
        msg, addr = sock.recvfrom(2048)
        server_handle_received_msg(sock, msg, addr)
