import threading
from socket import *

from ChatApp.models import User, Message
from ChatApp.msg import Msg, MsgType
from ChatApp.settings import TIMEOUT, DEBUG
from ChatApp.utils import get_timestamp


def send(msg, receiver):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    msg.to = receiver
    msg.send(sock)

    if msg.type_ == MsgType.UPDATE_TABLE:
        pass
    elif msg.type_ == MsgType.SEND_ALL:
        # TODO
        pass


def broadcast(msg: Msg):
    receivers = msg.get_receiver_list()
    threads = []

    for receiver in receivers:
        thread = threading.Thread(target=send, args=(msg, receiver, ))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def server_handle_received_msg(socket, msg, addr):
    rcv_msg = Msg.unpack(msg)

    if DEBUG:
        print(addr, rcv_msg.__dict__)

    type_ = rcv_msg.type_
    if type_ == MsgType.CREATE:
        user = User(rcv_msg.from_, addr[0], int(rcv_msg.content))
        user.save_or_update()
        msg = Msg(to=rcv_msg.from_, type_=MsgType.CREATED, addr=addr)
        msg.send(socket)

        msg = Msg(content=User.get_all(),
                  type_=MsgType.UPDATE_TABLE)

        broadcast(msg)
    elif type_ == MsgType.STORE:
        message = Message(rcv_msg.content,
                          rcv_msg.from_,
                          rcv_msg.to,
                          timestamp=get_timestamp())
        message.save()

        user = User.get_by_name(rcv_msg.to)
        if user:
            user.status = "no"
            user.save_or_update()
            Msg(type_=MsgType.STORE_ACK, addr=addr).send(socket)
            msg = Msg(content=[user.__dict__],
                      type_=MsgType.UPDATE_TABLE)
            broadcast(msg)
    elif type_ == MsgType.SEND_ALL:
        rcv_msg.to_server = False
        broadcast(rcv_msg)


def server_main(port: int):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", port))

    while True:
        msg, addr = sock.recvfrom(2048)
        server_handle_received_msg(sock, msg, addr)
