#!/usr/bin/env python

__author__ = "Maxime-Andrea Gouet and Pierre-Emmanuel Patry"
__copyright__ = "Copyright 2019, Maxime-Andrea Gouet & Pierre-Emmanuel Patry"
__credits__ = ["Maxime-Andrea Gouet", "Pierre-Emmanuel Patry"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Pierre-Emmanuel Patry"

import time
import argparse
from socket import *
from threading import Thread

import socket
from client import *
from message import *


# List of users
users = dict()

# This function has it's own thread,
# it iterates over all users and send
# the oldest untransmitted message to
# the user.
def processMessages():
    while True:
        for i in list(users.keys()):
            users[i].sendAwaiting()
            if not users[i].running:
                users.pop(i, None)


def addConnection(clientSocket, addr):
    print("[INFO]: New connection from", addr)
    # Get the initial message
    data = clientSocket.recv(4096).decode()
    msg = fromStr(data)
    username = msg.data
    # Checking if username is already registered in user list.
    if msg.data.upper() in users.keys():
        print("[WARN]: User already recorded, attributing a new username...")
        username = msg.data + "1"
        i = 2
        while username.upper() in users.keys():
            username = msg.data + str(i)
            i += 1


    message = Message("SERVER", [username], username).serialize()
    # Send back the attributed username
    print("[INFO]: Sending confirmation for ", addr)
    clientSocket.send(message.encode())

    upper = username.upper()
    
    users[upper] = Client(username, clientSocket, addr)
    users[upper].start(users)
    print("[INFO]: Added user", username,"with address",addr,"to the list")

parser = argparse.ArgumentParser(description="Handle message from client and send back the message order")
parser.add_argument('-v', '--verbose', action="count", default=0, help='Increase output verbosity')
parser.add_argument('-p','--port', help='specify the port (default=12000)', default=12000, type=int, nargs='?',const=True, required=False)
parser.add_argument('-V','--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()

# Create a TCP socket
serverSocket = socket.socket(AF_INET,SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind(('', args.port))
serverSocket.listen(1)
print ('[INFO]:The server is ready to receive')

retransmitThread = Thread(target = processMessages)
retransmitThread.start()


while True:
    # Create a new thread with that connectionSocket and start it.
    socket,addr = serverSocket.accept()
    addConnection(socket, addr)
serverSocket.close()


# Stopping retransmit thread
retransmitThread.join()
    
