from socket import *


def client_main(name: str, server_ip: str, server_port: int, client_port: int):

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', client_port))
    server_address = (server_ip, server_port)
    msg = input(">>>")
    sock.sendto(msg.encode(), server_address)
    res = sock.recv(2048)
    print(res)


if __name__ == "__main__":
    client_main("xc", "localhost", 11451, 11450)
