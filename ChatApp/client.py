from csv import excel_tab
from struct import pack
import threading
from socket import *

from ChatApp.utils import pack_message, unpack_message
from ChatApp.models import User
from ChatApp.constants import TIMEOUT, DEBUG


def handle_sent_msg(msg):
    words = msg.split()
    if words[0] == "send" and len(words) >= 3:
        type_ = words.pop(0)
        name = words.pop(0)
        user = User.get_by_name(name)

        if not user:
            raise Exception

        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(TIMEOUT)
        snd_msg = pack_message(msg=" ".join(words), type_=type_)
        sock.sendto(snd_msg, user.addr)

        try:
            rcv_msg = sock.recv(2048)
            msg = unpack_message(rcv_msg)
            if msg.get("type_") == "ack":
                print(f">>> [Message received by <{user.name}>]")
            else:
                # TODO
                print("[No ACK from <{user.name}>, message sent to server.]")
        except Exception as e:
            # TODO logging system
            pass


def handle_received_msg(msg, addr, listen_sock):
    rcv_msg = unpack_message(msg)
    if rcv_msg.get("type_") == "send":
        print("test_user: ", rcv_msg.get("msg"))
        ack_msg = pack_message("", type_="ack")
        listen_sock.sendto(ack_msg, addr)


def client_send_msg():
    while True:
        msg = input(">>> ")
        handle_sent_msg(msg)


def client_receive_msg(listen_sock):
    while True:
        msg, addr = listen_sock.recvfrom(2048)
        handle_received_msg(msg, addr, listen_sock)


def client_main(name: str, server_ip: str, server_port: int, client_port: int):

    server_port = int(server_port)
    client_port = int(client_port)

    listen_sock = socket(AF_INET, SOCK_DGRAM)
    listen_sock.bind(("", client_port))

    receive = threading.Thread(target=client_receive_msg, args=(listen_sock, ))
    send = threading.Thread(target=client_send_msg)

    receive.start()
    send.start()

    receive.join()
    send.join()
