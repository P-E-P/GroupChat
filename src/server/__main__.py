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
from userlist import *


parser = argparse.ArgumentParser(description="Handle message from client and send back the message order")
parser.add_argument('-v', '--verbose', action="count", default=0, help='Increase output verbosity')
parser.add_argument('-p', '--port', help='specify the port (default=12000)', default=12000, type=int, nargs='?',const=True, required=False)
parser.add_argument('-V', '--version', action='version', version='%(prog)s 1.0')

userlist = parser.add_mutually_exclusive_group()
userlist.add_argument('-w', '--whitelist', type=str, default=None,required=False)
userlist.add_argument('-b', '--blacklist', type=str, default=None, required=False)

args = parser.parse_args()

if args.whitelist is not None:
    ulist = Userlist(True, args.whitelist)
elif args.blacklist is not None:
    ulist = Userlist(False, args.blacklist)
else:
    ulist = None

server = Server(args.port, ulist)
server.start()

ipt = input()
while ipt != "stop":
    if ipt == "send":
        print("Write the message you whish to send to all users (leave blank to cancel):")
        message = input()
        if message != "":
            server.sendAll(message)
    else:
        print("[ERR]: Command not found")
    ipt = input()

server.close()
