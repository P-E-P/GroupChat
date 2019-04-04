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
from queue import *

from message import *

# We're using a list as a thread pool.
Tlist = []
# List of users
users = dict({"SERVER":Queue()})

'''
This function is started from a new thread,
it retransmit all message in the user queue to
the user
'''
def retransmit(clientSocket, username):
    up = username.upper()
    while True:
        while not users[up].empty():
            clientSocket.send(users[up].get().serialize().encode())

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

    
    users[usrname.upper()] = Queue()
    print("[INFO]: Added user", usrname,"with address",addr,"to the list")

    message = Message("SERVER", [usrname], usrname).serialize()
    # Send back the attributed username
    print("[INFO]: Sending confirmation for ", addr)
    clientSocket.send(message.encode())

    retransmitThread = Thread(target = retransmit, args = (clientSocket, usrname))
    retransmitThread.start()

    while True:
        try:
            data = clientSocket.recv(4096).decode()
            msg = fromStr(data)
            if "SERVER" in msg.recipients and msg.data == "QUIT":
                print("[INFO]: Client", msg.sender,"disconnected")
                break;
            
            print("Received a new message from ", msg.sender, "to", msg.recipients, ": (", msg.time, ")", msg.data)
            # If no recipient specified, send to all
            if msg.recipients == set(['']):
                for key in users:
                    if(key != usrname.upper()):
                        users[key].put(msg)
            else:
                for recip in msg.recipients:
                    if recip in users:
                        users[recip.upper()].put(msg)


        except Exception as e:
            print(e)
            print("Connection to", usrname, "has been lost")
            break;

    # Stopping retransmit thread
    retransmitThread.join()
    # Removing user from the list
    users.pop(username.upper(), None)

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
