from socket import *
from ChatApp.models import User

from ChatApp.utils import pack_message, unpack_message

def server_handle_received_msg(sock, msg, addr):
    rcv_msg = unpack_message(msg)
    if rcv_msg.get("type_") == "first_reg":
        user = User(rcv_msg["msg"], addr[0], addr[1])
        user.save_or_update()
        msg = pack_message("", users=User.get_all(), type_="update_table")
        sock.sendto(msg, addr)


def server_main(port: int):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", port))

    while True:
        msg, addr = sock.recvfrom(2048)
        server_handle_received_msg(sock, msg, addr)
