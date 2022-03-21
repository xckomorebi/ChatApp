import threading
from socket import *

from ChatApp.models import User, Message
from ChatApp.msg import Msg, MsgType
from ChatApp.settings import TIMEOUT, DEBUG
from ChatApp.utils import get_timestamp


def send(msg: Msg, receiver):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    msg.to = receiver
    msg.send(sock)

    if msg.type_ == MsgType.UPDATE_TABLE:
        pass
    elif msg.type_ == MsgType.SEND_ALL:
        try:
            ack_msg = sock.recv(2048)
            if ack_msg.type_ == MsgType.SEND_ALL_ACK:
                pass
        except timeout:
            user = User.get_by_name(msg.to)
            user.status = "no"
            user.save_or_update()
            msg.to_message().save()


def broadcast(msg: Msg):
    receivers = msg.get_receiver_list()
    threads = []

    for receiver in receivers:
        thread = threading.Thread(target=send, args=(msg, receiver, ))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def server_handle_received_msg(sock, msg, addr):
    rcv_msg = Msg.unpack(msg)

    if DEBUG:
        print(addr, rcv_msg.__dict__)

    type_ = rcv_msg.type_
    if type_ == MsgType.REG:
        user = User(rcv_msg.from_, addr[0], int(rcv_msg.content))

        existing_user = User.get_by_name(rcv_msg.from_)
        need_update = (existing_user != user)

        msg = Msg(to=rcv_msg.from_, addr=addr)

        if existing_user == None:
            msg.type_ = MsgType.CREATED
        else:
            msg.type_ = MsgType.REG_ACK
        msg.content = Message.retrieve_by_name(user.name) or ""
        msg.send(sock)

        if need_update:
            user.save_or_update()

            if existing_user and user.addr != existing_user.addr:
                Msg(type_=MsgType.LOGOUT,
                    to=rcv_msg.from_,
                    addr=existing_user.addr).send(sock)

            msg = Msg(content=User.get_all(),
                    from_=user.name,
                    type_=MsgType.UPDATE_TABLE)

            broadcast(msg)

        Msg(content=User.get_all(),
            to=user.name,
            type_=MsgType.UPDATE_TABLE).send(sock)

    elif type_ == MsgType.STORE:
        message = Message(rcv_msg.content,
                          rcv_msg.from_,
                          rcv_msg.to,
                          type_="send",
                          timestamp=get_timestamp())
        message.save()

        user = User.get_by_name(rcv_msg.to)
        if user:
            user.status = "no"
            user.save_or_update()
            Msg(type_=MsgType.STORE_ACK, addr=addr).send(sock)
            msg = Msg(content=user.__dict__,
                      type_=MsgType.UPDATE_TABLE)
            broadcast(msg)

    elif type_ == MsgType.SEND_ALL:
        Msg(type_=MsgType.SEND_ALL_SERVER_ACK,
            addr=addr).send(sock)
        rcv_msg.to_server = False
        broadcast(rcv_msg)

    elif type_ == MsgType.DEREG:
        user = User.get_by_name(rcv_msg.from_)
        user.status = "no"
        user.save_or_update()
        Msg(type_=MsgType.DEREG_ACK, addr=addr).send(sock)
        msg = Msg(content=user.__dict__,
                  type_=MsgType.UPDATE_TABLE)
        broadcast(msg)


def server_main(port: int):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", port))

    while True:
        msg, addr = sock.recvfrom(2048)
        server_handle_received_msg(sock, msg, addr)
