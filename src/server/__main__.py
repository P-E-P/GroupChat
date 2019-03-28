#!/usr/bin/env python

__author__ = "Maxime-Andrea Gouet and Pierre-Emmanuel Patry"
__copyright__ = "Copyright 2019, Maxime-Andrea Gouet & Pierre-Emmanuel Patry"
__credits__ = ["Maxime-Andrea Gouet", "Pierre-Emmanuel Patry"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Pierre-Emmanuel Patry"
__email__ = "ppatry@csumb.edu"
__status__ = "Production"

import time
import argparse
from socket import *
from threading import Thread

from message import *

# We're using a list as a thread pool.
Tlist = []
# List of users
users = dict({"SERVER":[]})

def addConnection(clientSocket, addr):
    print("[INFO]: New connection from", addr)
    # Get the initial message
    data = clientSocket.recv(4096).decode()
    msg = fromStr(data)
    usrname = msg.data
    # Checking if username is already registered in user list.
    if msg.data.upper() in users.keys():
        print("[WARN]: User already recorded, attributing a new username...")
        usrname = msg.data + "1"
        i = 2
        while usrname.upper() in users.keys():
            usrname = msg.data + str(i)
            i += 1

    
    users[usrname.upper()] = []
    print("[INFO]: Added user", usrname,"with address",addr,"to the list")

    message = Message("SERVER", [usrname], usrname).serialize()
    # Send back the attributed username
    print("[INFO]: Sending confirmation for ", addr)
    clientSocket.send(message.encode())

    # TODO: Handle message loop until client disconnect
    while True:
        continue
    

parser = argparse.ArgumentParser(description="Handle message from client and send back the message order")
parser.add_argument('-v', '--verbose', action="count", default=0, help='Increase output verbosity')
parser.add_argument('-p','--port', help='specify the port (default=12000)', default=12000, type=int, nargs='?',const=True, required=False)
parser.add_argument('-V','--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()

# Create a TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind(('', args.port))
serverSocket.listen(1)
print ('[INFO]:The server is ready to receive')

while True:
    # Create a new thread with that connectionSocket and start it.
    Tlist.append(Thread(target = addConnection, args = serverSocket.accept()).start())
serverSocket.close()
