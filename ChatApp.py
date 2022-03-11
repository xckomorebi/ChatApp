#!/usr/bin/env python3

import argparse
from ChatApp.server import server_main
from ChatApp.client import client_main


def get_args():
    parser = argparse.ArgumentParser()
    callee = parser.add_mutually_exclusive_group()
    callee.add_argument("-s", "--server", metavar="PORT", nargs=1)
    callee.add_argument("-c", "--client", metavar=("IP", "PORT", "CLIENT_NAME"), nargs=3)
    args = parser.parse_args()
    return parser, args


def main():
    parser, args = get_args()
    if args.server:
        server_main(*args.server)
    elif args.client:
        client_main(*args.client)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
