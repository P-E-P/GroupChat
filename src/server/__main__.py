#!/usr/bin/env python

__author__ = "Maxime-Andrea Gouet and Pierre-Emmanuel Patry"
__copyright__ = "Copyright 2019, Maxime-Andrea Gouet & Pierre-Emmanuel Patry"
__credits__ = ["Maxime-Andrea Gouet", "Pierre-Emmanuel Patry"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Pierre-Emmanuel Patry"

import time
import argparse

from server import *

parser = argparse.ArgumentParser(description="Handle message from client and send back the message order")
parser.add_argument('-v', '--verbose', action="count", default=0, help='Increase output verbosity')
parser.add_argument('-p','--port', help='specify the port (default=12000)', default=12000, type=int, nargs='?',const=True, required=False)
parser.add_argument('-V','--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()

server = Server(args.port)
server.start()

ipt = input()
while ipt != "stop":
    if ipt == "send":
        print("Write the message you whish to send to all users (leave blank to cancel):")
        message = input()
        if message != "":
            server.sendAll(message)
    else:
        print("Command not found")
    ipt = input()

server.close()
