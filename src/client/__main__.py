#!/usr/bin/env python

__author__ = "Maxime-Andrea Gouet and Pierre-Emmanuel Patry"
__copyright__ = "Copyright 2019, Maxime-Andrea Gouet & Pierre-Emmanuel Patry"
__credits__ = ["Maxime-Andrea Gouet", "Pierre-Emmanuel Patry"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Pierre-Emmanuel Patry"

from threading import Thread
import argparse
import sys

from client import *
import command
import username
import log

def parseCommand(ipt):
    args = ipt.split(" ")
    if args[0] == "leave":
        client.running = False

def send(client):
    while client.running:
        ipt = input("")
        if(ipt.startswith(command.PREFIX)):
            parseCommand(ipt[1:])
        else:
            client.send(ipt)
def receive(client):
    while client.running:
        message = client.receive()
        print(message.sender,"(", message.time,"):",message.data)
        

if __name__ == '__main__':

    log.checkANSI()
    
    parser = argparse.ArgumentParser(description="Groupchat client")
    # User needs to set the hostname
    parser.add_argument('hostname',help="Specify your hostname")
    # Specify verbose level
    parser.add_argument('-v', '--verbose', action="count", default=0, help='Increase output verbosity')
    parser.add_argument('-p','--port', help='specify the port (default=12000)', default=12000, type=int, nargs='?',const=True, required=False)
    parser.add_argument('-u','--username', action='store', default=username.gen_wrd(), type=str, help = 'Specify your username.' )
    parser.add_argument('-V','--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    
    print("You chose the username:", args.username)

    client = Client(args.username)
    if not client.connect(args.hostname, args.port):
        sys.exit()

    log.info("Connected")

    rcvThread = Thread(target = receive, args=[client]).start()
    send(client)
    
    client.disconnect()
    
    log.info("Disconnected")
