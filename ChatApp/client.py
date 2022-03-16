import threading
from socket import *

from ChatApp.constants import DEBUG, TIMEOUT
from ChatApp.models import User
from ChatApp.utils import pack_message, unpack_message


def handle_sent_msg(msg, name, server_ip, server_port):
    words = msg.split()
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    if words[0] == "send" and len(words) >= 3:
        type_ = words.pop(0)
        name = words.pop(0)
        user = User.get_by_name(name)

        if not user:
            raise Exception

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
    elif words[0] == "first_reg":
        snd_msg = pack_message(name, type_="first_reg")
        addr = (server_ip, server_port)
        try:
            sock.sendto(snd_msg, addr)
            rcv_msg = sock.recv(2048)
            msg = unpack_message(rcv_msg)
            User.save_from_list(msg.get("users", []))
            print(">>> [Welcome, You are registered.]")
            print(">>> [Client table updated.]") # TODO this should be boardcast

    elif words[0] == "reg" and len(words) == 2:
        pass
    elif words[0] == "dereg":
        pass
    elif words[0] == "send_all":
        pass


def handle_received_msg(msg, addr, listen_sock):
    rcv_msg = unpack_message(msg)
    if rcv_msg.get("type_") == "send":
        print("test_user: ", rcv_msg.get("msg"))
        ack_msg = pack_message("", type_="ack")
        listen_sock.sendto(ack_msg, addr)


def client_send_msg(name, server_ip, server_port):
    msg = "first_reg"
    handle_sent_msg(msg, name, server_ip, server_port)
    while True:
        msg = input(">>> ")
        handle_sent_msg(msg, name, server_ip, server_port)


def client_receive_msg(listen_sock):
    while True:
        msg, addr = listen_sock.recvfrom(2048)
        handle_received_msg(msg, addr, listen_sock)


def client_main(name: str, server_ip: str, server_port: int, client_port: int):

    server_port = int(server_port)
    client_port = int(client_port)

    listen_sock = socket(AF_INET, SOCK_DGRAM)
    listen_sock.bind(("", client_port))


    # TODO switch to select.select()
    receive = threading.Thread(target=client_receive_msg,
                               args=(listen_sock, ))
    send = threading.Thread(target=client_send_msg,
                            args=(name, server_ip, server_port, ))

    receive.start()
    send.start()

    receive.join()
    send.join()
