import threading
from socket import *

from ChatApp.models import User, Message
from ChatApp.msg import Msg, MsgType
from ChatApp.settings import TIMEOUT, DEBUG
from ChatApp.utils import get_timestamp


def send(msg: Msg, receiver):
    global send_all_need_update
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    msg.to = receiver
    msg.send(sock)

    if msg.type_ == MsgType.UPDATE_TABLE:
        pass
    elif msg.type_ == MsgType.SEND_ALL:
        try:
            ack_msg = sock.recv(2048)
            if Msg.unpack(ack_msg).type_ == MsgType.SEND_ALL_ACK:
                pass
        except timeout:
            user = User.get_by_name(receiver)
            user.status = "no"
            send_all_need_update = True
            user.save_or_update()
            msg.to_message(receiver).save()
    return sock


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
        try:
            test_sock = send(Msg(type_=MsgType.TEST, to=rcv_msg.to), rcv_msg.to)
            rcv_pkt = test_sock.recv(2048)
            if Msg.unpack(rcv_pkt).type_ == MsgType.TEST:
                Msg(to=rcv_msg.from_,
                    type_=MsgType.USER_EXIST,
                    addr=addr).send(sock)

                user = User.get_by_name(rcv_msg.to)
                user.status = "yes"
                user.save_or_update()

                Msg(content=User.get_all(),
                    to=rcv_msg.from_,
                    type_=MsgType.UPDATE_TABLE).send()

                return
        except timeout:
            pass

        message = Message(rcv_msg.content,
                          rcv_msg.from_,
                          rcv_msg.to,
                          type_="send",
                          timestamp=get_timestamp())
        message.save()

        user = User.get_by_name(rcv_msg.to)
        if user:
            if user.status == "yes":
                user.status = "no"
                user.save_or_update()
                Msg(type_=MsgType.STORE_ACK, addr=addr).send(sock)
                msg = Msg(content=user.__dict__,
                        type_=MsgType.UPDATE_TABLE)
                broadcast(msg)
            else:
                Msg(type_=MsgType.STORE_ACK, addr=addr).send(sock)

    elif type_ == MsgType.SEND_ALL:
        global send_all_need_update
        send_all_need_update = False
        Msg(type_=MsgType.SEND_ALL_SERVER_ACK,
            addr=addr).send(sock)
        rcv_msg.to_server = False
        broadcast(rcv_msg)

        if DEBUG:
            print(User.get_all_inactive_users())

        for user_dict in User.get_all_inactive_users():
            rcv_msg.to_message(user_dict.get("name")).save()

        if send_all_need_update:
            msg = Msg(content=User.get_all(),
                     type_=MsgType.UPDATE_TABLE)
            broadcast(msg)

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
