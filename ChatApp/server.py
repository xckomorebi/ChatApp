from socket import *


def server_main(port: int):
    """"""

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", port))

    while True:
        msg, addr = sock.recvfrom(2048)
        sock.sendto(msg * 2, addr)


if __name__ == "__main__":
    server_main(11451)
