import os
import threading
from socket import *

from ChatApp.settings import TIMEOUT, DEBUG
from ChatApp.models import User
from ChatApp.msg import Msg, MsgType


def handle_sent_msg(input_):
    global STATUS
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    msg = Msg.from_input(input_)
    type_ = msg.type_

    if type_ == MsgType.SEND:
        try:
            msg.send(sock)
            rcv_packet = sock.recv(2048)
            rcv_msg = Msg.unpack(rcv_packet)
            if rcv_msg.type_ == MsgType.ACK:
                print(f">>> [Message received by <{rcv_msg.from_}>]")
        except timeout:
            print(f">>> [No ACK from <{msg.to}>, message sent to server.]")
            msg.type_ = MsgType.STORE
            msg.to_server = True
            msg.send(sock)
            try: 
                rcv_msg = Msg.unpack(sock.recv(2048))
                if rcv_msg.type_ == MsgType.STORE_ACK:
                    print(">>> [Message received by the server and saved.]")
            except timeout:
                pass
    elif type_ == MsgType.CREATE:
        for retry in range(5):
            try:
                msg.send(sock)
                rcv_packet = sock.recv(2048)
                rcv_msg = Msg.unpack(rcv_packet)
                if rcv_msg.type_ == MsgType.CREATED:
                    print(">>> [Welcome, You are registered.]")
                    return
            except timeout:
                if DEBUG:
                    print(f">>> retry {retry+1}: not respond, exit after 5 retries")
        print(">>> [Server not responding]\n>>> [Exiting]")
        os._exit(0)
    elif type_ == MsgType.DEREG:
        msg.send(sock)
        STATUS = False
    elif type_ == MsgType.REG:
        msg.send(sock)
        STATUS = True

    elif type_ == MsgType.SEND_ALL:
        try:
            msg.send(sock)
        except Exception as e:
            pass


def handle_received_msg(msg, addr, socket):
    rcv_msg = Msg.unpack(msg)
    type_ = rcv_msg.type_

    if type_ == MsgType.SEND:
        print(f"{rcv_msg.from_}: {rcv_msg.content}\n>>> ", end="")
        ack_msg = Msg(type_=MsgType.ACK,
                      to=rcv_msg.from_,
                      addr=addr)

        ack_msg.send(socket)
    elif type_ == MsgType.UPDATE_TABLE:
        User.save_from_list(rcv_msg.content)
        print("[Client table updated.]\n>>> ", end="")
    elif type_ == MsgType.SEND_ALL:
        print(f"[Channel_Message <{rcv_msg.from_}>: {rcv_msg.content}]\n>>> ", end="")


def client_send_msg():
    msg = f"create {CLIENT_PORT}"
    handle_sent_msg(msg)
    while True:
        msg = input(">>> ")
        if not msg:
            continue

        if STATUS:
            handle_sent_msg(msg)
        else:
            if Msg.from_input(msg).type_ == MsgType.REG:
                handle_sent_msg(msg)
            else:
                print(">>> [you are offline.]")


def client_receive_msg(listen_sock):
    while True:
        if STATUS:
            msg, addr = listen_sock.recvfrom(2048)
            handle_received_msg(msg, addr, listen_sock)
        else:
            pass


def client_main(name: str, server_ip: str, server_port: int, client_port: int):
    server_port = int(server_port)
    client_port = int(client_port)

    global CLIENT_PORT
    global STATUS
    CLIENT_PORT = client_port
    STATUS = True

    listen_sock = socket(AF_INET, SOCK_DGRAM)
    listen_sock.bind(("", client_port))

    Msg.server_addr = (server_ip, server_port)
    Msg.name = name

    # TODO switch to select.select()
    receive = threading.Thread(target=client_receive_msg,
                               args=(listen_sock, ))
    send = threading.Thread(target=client_send_msg)

    receive.start()
    send.start()

    receive.join()
    send.join()
