#!/usr/bin/env python

__author__ = "Maxime-Andrea Gouet and Pierre-Emmanuel Patry"
__copyright__ = "Copyright 2019, Maxime-Andrea Gouet & Pierre-Emmanuel Patry"
__credits__ = ["Maxime-Andrea Gouet", "Pierre-Emmanuel Patry"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Pierre-Emmanuel Patry"
__email__ = "ppatry@csumb.edu"
__status__ = "Production"

from socket import *
import argparse

import username

parser = argparse.ArgumentParser(description="Groupchat client")
# User needs to set the hostname
parser.add_argument('hostname',help="Specify your hostname")
# Specify verbose level
parser.add_argument('-v', '--verbose', action="count", default=0, help='Increase output verbosity')
parser.add_argument('-p','--port', help='specify the port (default=12000)', default=12000, type=int, nargs='?',const=True, required=False)
parser.add_argument('-u','--username', action='store', default=username.gen_wrd(), type=str, help = 'Specify your username.' )
parser.add_argument('-V','--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

print("Your username is:", args.username)

# Create a new TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# Connect to the server
clientSocket.connect((args.hostname,args.port))
sentence = "Client " + clientNo + ": " + args.name
# Send the message
input("Press enter to send the message...")
clientSocket.send(sentence.encode())
