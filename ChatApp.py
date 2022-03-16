#!/usr/bin/env python3
import os
import argparse
from ChatApp.exceptions import InvalidIpException, InvalidPortException
from ChatApp.server import server_main
from ChatApp.client import client_main
from ChatApp.utils import check_ip, check_port


def get_args():
    parser = argparse.ArgumentParser()
    callee = parser.add_mutually_exclusive_group()
    callee.add_argument("-s", "--server", metavar="PORT", nargs=1)
    callee.add_argument("-c", "--client", metavar=("NAME", "SERVER-IP", "SERVER-PORT", "CLIENT-PORT"), nargs=4)
    args = parser.parse_args()
    return parser, args


def main():
    parser, args = get_args()
    try:
        if args.server:
            port = check_port(args.server[0])
            server_main(port)
        elif args.client:
            name, server_ip, server_port, client_port = args.client
            ip = check_ip(server_ip)
            server_port = check_port(server_port)
            client_port = check_port(client_port)
            client_main(name, ip, server_port, client_port)
        else:
            parser.print_help()
    except InvalidIpException:
        print("You should enter a valid IP address!")
    except InvalidPortException:
        print("Port number should be an integer between 1024 and 65535!")
    except KeyboardInterrupt:
        print("Bye!!")
        os._exit(0)


if __name__ == "__main__":
    main()
